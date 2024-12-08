from pydantic import BaseModel, EmailStr


class Profile_Schema(BaseModel):
    fullname: str
    email: EmailStr
    bio: str

    class Config:
        form_attributes = True
