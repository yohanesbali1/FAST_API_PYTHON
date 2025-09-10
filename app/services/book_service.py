from math import ceil
from anyio import Path
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookRequest, ShowBookResponse
from fastapi import UploadFile, HTTPException, Request
import os
from uuid import uuid4
from PIL import Image

UPLOAD_DIR = Path("app/uploads/books")
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
            picture=filename,
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


def update_book(
    db: Session, data: BookRequest, book_id: int, picture: UploadFile = None
):
    try:
        db_data = db.query(Book).filter(Book.id == book_id).first()
        if not db_data:
            raise HTTPException(status_code=404, detail="Book not found")

        # Update data teks
        db_data.title = data.title
        db_data.author = data.author
        db_data.description = data.description

        # Update picture jika ada
        if picture:
            # Hapus file lama jika ada
            if db_data.picture:
                old_file_path = os.path.join(UPLOAD_DIR, db_data.picture)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Proses gambar (kompres + simpan)
            filename = f"{uuid4().hex}.jpg"
            file_path = os.path.join(UPLOAD_DIR, filename)
            image = Image.open(picture.file)
            image = image.convert("RGB")
            image.save(file_path, "JPEG", optimize=True, quality=70)

            db_data.picture = filename

        db.commit()
        db.refresh(db_data)
        return {
            "status": 200,
            "message": "Book updated successfully",
        }

    except Exception as e:
        db.rollback()
        if picture:
            file_path = os.path.join(
                UPLOAD_DIR, f"{book_id}{os.path.splitext(picture.filename)[1]}"
            )
            if os.path.exists(file_path):
                os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to update book: {e}")


def get_book(db: Session, request: Request, search: str, page: int, per_page: int):
    query = db.query(Book)

    # Filter search
    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) | (Book.author.ilike(f"%{search}%"))
        )

    # Total data
    total = query.count()
    total_pages = ceil(total / per_page) if total > 0 else 1

    # Pagination
    books = query.offset((page - 1) * per_page).limit(per_page).all()

    # Base URL untuk gambar
    base_url = str(request.base_url) + "uploads/"

    # Build response data
    data = []
    for book in books:
        picture_url = base_url + book.picture if book.picture else None
        data.append(
            ShowBookResponse(
                id=book.id,
                title=book.title,
                author=book.author,
                description=book.description,
                picture=picture_url,
            )
        )

    # Meta pagination
    meta = {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }

    return {"data": data, "meta": meta}


def show_book(book_id: int, request: Request, db: Session):
    data = db.query(Book).filter(Book.id == book_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Book not found")
    if data.picture:
        base_url = str(request.base_url) + "uploads/"
        data.picture = base_url + data.picture
    return {"data": ShowBookResponse(**data.__dict__)}


def delete_book(db: Session, book_id: int):
    db_data = db.query(Book).filter(Book.id == book_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_data)
    db.commit()
    return {"status": 200, "message": "Book deleted successfully"}
