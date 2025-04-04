from dataclasses import dataclass
from typing import Optional,List,Dict

@dataclass
class HadithSchema:
    id : str
    title : str 
    hadith_text : str
    author_hadith : str
    hadith_type:str
    languages : Optional[List[Dict]]
    created : int
    updated : int
    hijri_time : str

