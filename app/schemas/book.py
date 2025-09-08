from pydantic import BaseModel
from fastapi import  Form

class BookRequest(BaseModel):
    title: str
    author: str
    description: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        author: str = Form(...),
        description: str = Form(...),
    ):
        return cls(title=title, author=author, description=description)


class BookResponse(BaseModel):
    id: int
    title: str
    description: str
    author: str

