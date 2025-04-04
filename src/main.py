import logging
import time
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from fastapi import FastAPI,APIRouter,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from .exceptions.exception import BaseAPIException
from .controller.auth import auth_router
from .controller.user import user_router
from .controller.ayah import ayah_router
from .controller.transcript import transcript_router
from .controller.translate import translate_router
from .controller.hadis import hadis_router
from .controller.like import like
from .controller.file import file_router
from .controller.dhikr import dhikr_router
from .repository.db import setup_db
# from .repository.db import get_database
from .constants import Errors
# db = get_database()
# repo = UserRepository(db=db)
# service =UserService(repository=repo)
app = FastAPI()
api_v1_router  = APIRouter(prefix="/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(ayah_router)
api_v1_router.include_router(hadis_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(ayah_router)
api_v1_router.include_router(transcript_router)
api_v1_router.include_router(translate_router)
api_v1_router.include_router(like)
api_v1_router.include_router(file_router)
api_v1_router.include_router(dhikr_router)
app.include_router(api_v1_router)

##crate default user of project
@app.on_event("startup")
async def data_base():
    await setup_db()

    
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust the frontend URL as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(
    # for example logging.getLogger("example_logger")  name ="example_logger"
    level=logging.DEBUG,  # Set the desired logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Display logs in the console
        # You can add other handlers here, like logging.FileHandler() to write logs to a file
    ],
)

@app.get("/",response_model=dict)
async def root():
    return {"success":"hello world"}


# Access the Swagger UI
@app.get("/docs", include_in_schema=False)
async def override_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Example")



@app.exception_handler(BaseAPIException)
async def base_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={**exc.model().dict(), "timestamp": time.time()},
    )


@app.exception_handler(InvalidId)
async def invalid_id_exception_handler(request: Request, exc: InvalidId):
    return JSONResponse(
        status_code=400,
        content={"message": Errors.invalid_id, "timestamp": time.time()},
    )


@app.exception_handler(DuplicateKeyError)
async def duplicate_key_exception_handler(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=208,
        content={"message": Errors.alr_exists, "timestamp": time.time()},
    )

