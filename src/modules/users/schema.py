from pydantic import BaseModel, EmailStr, Field


class User_Schema(BaseModel):
    fullname: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=256)

    class Config:
        from_attributes = True

