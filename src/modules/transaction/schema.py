from pydantic import BaseModel


class Transaction_Schema(BaseModel):
    book_id: str

    class Config:
        form_attributes = True
