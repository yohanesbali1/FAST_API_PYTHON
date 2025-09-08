from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookRequest 
from fastapi import UploadFile, HTTPException
import os
from uuid import uuid4
from PIL import Image

UPLOAD_DIR = "uploads/books"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def create_book(db: Session, data: BookRequest, picture: UploadFile):    
    filename = f"{uuid4().hex}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        # 1. Simpan record di DB (tapi belum commit)
        db_data = Book(
            title=data.title,
            author=data.author,
            description=data.description,
            picture=file_path,
        )
        db.add(db_data)
        db.flush()  # flush dulu biar dapat ID tapi belum commit

        # 2. Proses gambar (kompres + simpan)
        image = Image.open(picture.file)
        image = image.convert("RGB")
        image.save(file_path, "JPEG", optimize=True, quality=70)

        # 3. Commit jika semua berhasil
        db.commit()
        db.refresh(db_data)
        return db_data

    except Exception as e:
        # Hapus file kalau sudah sempat dibuat
        if os.path.exists(file_path):
            os.remove(file_path)

        # Rollback database
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload book: {e}")

def get_book(db: Session):
    return db.query(Book).all()

def delete_book(db: Session, book_id: int):
    db.query(Book).filter(Book.id == book_id).delete()
    db.commit()
