from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserCreate(BaseModel):
    firstname: str = Field(..., description="user name", min_length=3, max_length=80)
    lastname: str = Field(..., description="last name", min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(..., description="password", min_length=5, max_length=20)
    phone_number: str = Field(..., description="phone number")
    region: str = Field(default="Almaty", description="region",min_length=1)

    @validator("password")
    def validate_password(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() and not char.islower() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isalnum() for char in value):
            raise ValueError("Password must contain at least one special character")
        return value
    
    class Config:
        json_schema_extra ={
            "example":{
                "firstname":"Qazaq",
                "lastname":"Style",
                "email":"qazaq@gmail.com",
                "password":"QR_@911216",
                "phone_number":"+7707888888888",
                "region":"QAZAQ"
            }
        }



class UserUpdate(BaseModel):
    firstname: Optional[str] = Field(None, description="user name")
    lastname: Optional[str] = Field(None, description="last name")
    phone_number: Optional[str] = Field(None, description="phone number")
    region: Optional[str] = Field(None, description="region")

    class Config:
        json_schema_extra ={
            "example":{
                "firstname":"Qazaq",
                "lastname":"Style",
                "phone_number":"+7707888888888",
                "region":"QAZAQ"
            }
        }
    
    
