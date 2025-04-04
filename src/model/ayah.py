from typing import List
from pydantic import BaseModel,Field
from .hadith import DefaultModel

class AyahCreate(BaseModel):
    surah_title :str= Field(...,description="surah title",min_length=2)
    surah_ayah:str = Field(...,description="surah ayah",min_length=1)
    arabic_text :str = Field(...,description="arabic text of surah",min_length=1)
    languages:List[DefaultModel]

    class Config:
        json_schema_extra ={
            "example":{
                "surah_title":"Baqara",
                "surah_ayah":"1:12",
                "arabic_text":"text of arabic",
                "languages":[
                    {
                        "transcript": "Субханаллах",
                        "translate_text": "Алла тағала кемшіліктен пәк",
                        "lang": "QAZ"
                    }
                ]
            }
        }

class DHikrCreate(BaseModel):
    title:str = Field(...,description="title of dhikr")
    arabic_text:str =Field(...,description="dikr text")
    languages:List[DefaultModel]

    class Config:
        json_schema_extra ={
            "example":{
                "title":"dhikr title",
                "arabic_text":"text of arabiec",
                "languages":[
                    {
                        "transcript": "Субханаллах",
                        "translate_text": "Алла тағала кемшіліктен пәк",
                        "lang": "QAZ"
                    }
                ]
            }
        }