from pydantic import BaseModel, EmailStr, Field, field_validator


class Signup_schema(BaseModel):
    fullname: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=256)

    class Config:
        from_attributes = True


class Login_Schema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=256)

    class Config:
        from_attributes = True


class Resend_email_Schema(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class Forgot_Password_Schema(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class Reset_Password_Schema(BaseModel):
    token: str
    password: str = Field(..., min_length=8, max_length=256)
    confirmPassword: str

    @field_validator("confirmPassword")
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Password do not match")
        return v

    class Config:
        from_attributes = True
