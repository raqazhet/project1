from pydantic import BaseModel, Field
from typing import List,Optional

class DefaultModel(BaseModel):
    transcript: str = Field(..., description="transcript of text")
    translate_text: str = Field(..., description="text translate")
    lang: str = Field(default="QAZ", description="lang of text")

    class Config:
        json_schema_extra = {
            "example": {
                "transcript": "Субханаллах",
                "translate_text": "Алла тағала кемшіліктен пәк",
                "lang": "QAZ"
            }
        }

class HadithCreate(BaseModel):
    title: str = Field(..., description="hadith title")
    hadith_text: str = Field(..., description="hadith text")
    author_hadith: str = Field(..., description="name of Nararator")
    hadith_type: str = Field(..., description="hadith type")
    languages: List[DefaultModel]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Тарауық",
                "hadith_text": "arabsha text",
                "author_hadith": "author of haidth",
                "hadith_type": "hadith type (sauda, tb)",
                "languages": [
                    {
                        "transcript": "Субханаллах",
                        "translate_text": "Алла тағала кемшіліктен пәк",
                        "lang": "QAZ"
                    }
                ]
            }
        }


class HadithUpdate(BaseModel):
    title:Optional[str] 
    hadith_text: Optional[str] 
    author_hadith : Optional[str] 
    hadith_type:Optional[str]
    languages:Optional[List[DefaultModel]]

    class Config:
        json_schema_extra={
            "example": {
                "title":"Тарауық",
                "hadith_text":"arabsha text",
                "author_hadith":"author of haidth",
                "hadith_type":"hadith type (sauda, tb)",
                "languages":[
                    {
                        "transcript":"Субханаллах",
                        "translate_text":"Алла тағала кемшіліктен пәк",
                        "lang":"QAZ"
                    }
                ]
            }
        }
