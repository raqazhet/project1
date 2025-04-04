from dataclasses import dataclass

@dataclass
class TrascriptSchema:
    id:str
    ayah_id:str
    transcript:str
    lang:str
    created:int
    updated:int
    hijri_time:str
    

@dataclass
class TranslateSchema:
    id:str
    ayah_id:str
    text:str
    lang:str
    created:int
    updated:int
    hijri_time:str

