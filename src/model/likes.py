from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class LikeCreate(BaseModel):
    # client_id:str=Field(...,description="client id")
    card_id:str= Field(...,description="card id")
    card_type:str=Field(...,description="card type for example hadith e.tc")
    created:int = Field(default=int(datetime.utcnow().timestamp()))

    class Config:
        json_schema_extra ={
            "example":{
                "card_id":"123jfweu324",
                "card_type":"hadith"
            }
        }
    

class UpdateLike(BaseModel):
    # client_id:Optional[str]
    card_id:Optional[str]
    updated:int = Field(default=int(datetime.utcnow().timestamp()))

