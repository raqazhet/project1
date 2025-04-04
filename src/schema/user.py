from dataclasses import dataclass


@dataclass
class UserResponse:
    id: str
    firstname: str
    lastname: str
    email: str
    created: int
    updated: int
    last_read_zikrid: str
    hash_password: str
    phone_number: str
    region: str
    role: str
    hijri_time:str

    class Config:
        orm_mode = True
