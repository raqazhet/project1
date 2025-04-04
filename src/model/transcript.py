from pydantic import BaseModel,Field
from typing import Optional

class TranscriptCreate(BaseModel):
    ayah_id:str=Field(...,description="ayah id",min_length=6)
    transcript:str=Field(...,description="transcript of text")
    lang:str=Field(default="QAZ",description="languages of transcript")


class UpdateTranscript(BaseModel):
    transcript:Optional[str]
    lang:Optional[str]



#Class For translate of text
    
class TranslateCreate(BaseModel):
    ayah_id:str = Field(...,description="ayah it",min_length=1)
    text:str =Field(...,description="text of translate",min_length=1)
    lang:str=Field(default='QAZ',description="lang of text",min_length=1)

class TransLateUpdate(BaseModel):
    text:Optional[str] =Field(default="text",description="text of translate")
    lang:Optional[str]=Field(default='QAZ',description="lang of text")
