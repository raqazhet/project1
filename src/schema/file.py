from dataclasses import dataclass

@dataclass
class FileSchema:
    id:str
    filename:str
    title:str
    description:str
    created:int