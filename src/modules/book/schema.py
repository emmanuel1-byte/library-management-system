from pydantic import BaseModel
from typing import List


class Book_Schema(BaseModel):
    title: str
    author: List[str]
    genre: str
    isbn: str
    available_copies: int

    class Config:
        form_attributes = True
