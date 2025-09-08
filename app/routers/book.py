from fastapi import APIRouter, Depends,File,UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookRequest, BookResponse
from app.services import book_service
from app.core.security import require_permission,get_current_user

router = APIRouter(
    tags=["Books"],
    dependencies=[Depends(require_permission("custom_book"))]
)

@router.post("", response_model=BookResponse)
def create_book(
    data: BookRequest = Depends(BookRequest.as_form),
    picture: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if picture.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only images are allowed")

    return book_service.create_book(db, data, picture)

@router.get("", response_model=list[BookResponse])
def get_book(  db: Session = Depends(get_db)  ):
    return book_service.get_book(db)


@router.delete("/{book_id}", response_model=list[BookResponse])
def delete_book(book_id: int,  db: Session = Depends(get_db)):
    return book_service.delete_book(db,book_id)