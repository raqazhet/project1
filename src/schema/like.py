from dataclasses import dataclass

@dataclass
class LikeResponse:
    id:str
    client_id:str
    card_id:str
    card_type:str
    created:int
    updated:int