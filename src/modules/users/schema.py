from pydantic import BaseModel, EmailStr, Field
from typing import List


class User_Schema(BaseModel):
    fullname: str
    email: EmailStr
    roles: List[str]
    password: str = Field(..., min_length=8, max_length=256)

    class Config:
        from_attributes = True
        

class Update_User_Schema(BaseModel):
    fullname: str
    email: EmailStr
    roles: List[str]

    class Config:
        from_attributes = True
        
        

