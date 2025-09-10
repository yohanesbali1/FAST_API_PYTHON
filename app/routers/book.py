from typing import Optional
from fastapi import APIRouter, Depends, File, Query, UploadFile, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import book
from app.schemas.book import BookRequest, BookResponse, ShowBookResponse
from app.services import book_service
from app.core.security import require_permission, get_current_user

router = APIRouter(
    tags=["Books"], dependencies=[Depends(require_permission("custom_book"))]
)


@router.post("", response_model=BookResponse)
def create_book(
    data: BookRequest = Depends(BookRequest.as_form),
    picture: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if picture.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only images are allowed")

    return book_service.create_book(db, data, picture)


@router.put("/{book_id}")
def update_book(
    book_id: int,
    data: BookRequest = Depends(BookRequest.as_form),
    picture: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    if picture and picture.content_type not in [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]:
        raise HTTPException(status_code=400, detail="Only images are allowed")

    return book_service.update_book(db, data, book_id, picture)


@router.get("")
def get_book(
    request: Request,
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by title or author"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    return book_service.get_book(db, request, search, page, per_page)


@router.get("/{book_id}")
def show_book(book_id: int, request: Request, db: Session = Depends(get_db)):
    return book_service.show_book(book_id, request, db)


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.delete_book(db, book_id)
