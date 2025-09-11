from typing import Optional
from pydantic import BaseModel
from fastapi import Form


class BookRequest(BaseModel):
    title: str 
    author: str
    description: str 
    
    @classmethod
    def as_form(
        cls,
        title: str = Form(..., example="Buku Python"),
        author: str = Form(..., example="John Doe"),
        description: str = Form(..., example="Deskripsi singkat buku Python"),
    ):
        return cls(title=title, author=author, description=description)

class BookUpdateRequest(BaseModel):
    title: Optional[str] = Form(None)
    author: Optional[str] = Form(None)
    description: Optional[str] = Form(None)

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(None,example="Buku Python"),
        author: Optional[str] = Form(None, example="John Doe"),
        description: Optional[str] = Form(None, example="Deskripsi singkat buku Python"),
    ):
        return cls(title=title, author=author, description=description)


class BookResponse(BaseModel):
    id: int
    title: str
    description: str
    author: str


class ShowBookResponse(BookResponse):
    picture: str = None
