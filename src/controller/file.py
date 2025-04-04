from fastapi import APIRouter, File, UploadFile, HTTPException,Depends
from fastapi.responses import StreamingResponse
from datetime import date
from typing import Optional
import boto3
import os
import io
from ..utils.utils import allowed_file
from ..config.config import AWS_ENDPOIN_URL,AWS_SECRET_KEY,AWS_ACCESS_KEY_ID,AWS_BUCKET_NAME
from ..service.file import FileService
from ..schema.user import UserResponse
from ..dependencies import get_file_service,get_current_user
from ..redis import redis_get

file_router = APIRouter(prefix="/file",tags=['file'])

# Настройки CORS для разрешения запросов с любого источника (в реальном приложении уточните)

s3 = boto3.resource('s3',
    endpoint_url=AWS_ENDPOIN_URL,  
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Получаем объект корзины
boto_test_bucket = s3.Bucket(AWS_BUCKET_NAME)

@file_router.post("/uploadfile/")
async def create_upload_file(
    title: Optional[str] = None,
    description: Optional[str] = None,
    service: FileService = Depends(get_file_service),
    current_user:UserResponse=Depends(get_current_user),
    file: UploadFile = File(...)
): 
    if current_user.role !='admin':
        raise HTTPException(status_code=403,detail="you don't have permission")
    if not await allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Недопустимый формат файла")

    # Сохраняем файл во временной директории перед загрузкой в Wasabi
    file_path = f"tmp_{file.filename}"
    with open(file_path, "wb") as temp_file:
        temp_file.write(file.file.read())
    # Загружаем файл в Wasabi
    boto_test_bucket.upload_file(file_path,file.filename)
    # Удаляем временный файл
    os.remove(file_path)
    data_file={
        "filename":file.filename,
        "title":title,
        "description":description
    }
    result = await service.create_file(data=data_file)
    return {"message": "file uploaded successfully",
            "filename":file.filename,
            "created_id":result}

@file_router.get("/getfile/{id}")
async def get_file(
    id: str,
    service: FileService = Depends(get_file_service)
):
    try:
        # Загружаем файл из Wasabi
        file_data = await service.get_file_by_id(id)
        obj = boto_test_bucket.Object(file_data.filename)  # Use dot notation
        file_content = obj.get()['Body'].read()
        # Возвращаем файл клиенту
        return StreamingResponse(io.BytesIO(file_content), media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Файл не найден {e}")


@file_router.delete("/{id}",response_model=dict)
async def delete_file_by_id(id:str,
                    service:FileService=Depends(get_file_service),
                    current_user:UserResponse=Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code = 403,detail="you don't have permission")
    file_data = await service.get_file_by_id(id)
# Удаляем файл из Wasabi
    obj = boto_test_bucket.Object(file_data.filename)
    obj.delete()
    deleted_id = await service.delete_file_by_id(id)
    return {"id":deleted_id}


@file_router.get("/day/image")
async def get_day_of_image(service: FileService = Depends(get_file_service)):
    try:
        key = f"{date.today().isoformat()}_file"
        file_data = await redis_get(key=key)
        obj = boto_test_bucket.Object(file_data['filename'])  # Use dot notation
        file_content = obj.get()['Body'].read()
        # Возвращаем файл клиенту
        return StreamingResponse(io.BytesIO(file_content), media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Файл не найден {e}")



