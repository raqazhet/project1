from dataclasses import dataclass
from typing import Optional,List,Dict

@dataclass
class AyahSchema:
    id:str
    surah_title: str
    surah_ayah: str
    arabic_text: str
    languages:Optional[List[Dict]]
    created: int
    updated: int
    hijri_time: int
