from typing import Optional
from fastapi import APIRouter, Depends, File, Query, UploadFile, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookRequest, BookResponse, BookUpdateRequest, ShowBookResponse
from app.services import book_service
from app.core.security import require_permission, get_current_user

router = APIRouter(
    tags=["Books"], dependencies=[Depends(require_permission("custom_book"))]
)


@router.post("", 
             status_code=status.HTTP_201_CREATED,
             response_model=BookResponse,
             description="""
Endpoint untuk membuat buku baru.  

- **title**: Judul buku, wajib diisi  
- **author**: Nama penulis buku, wajib diisi  
- **description**: Deskripsi singkat tentang buku, wajib diisi  
- **picture**: Gambar buku, wajib diisi

Jika berhasil:
- **201 Created** → Mengembalikan data buku baru yang dibuat  

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa
- **422 Validation Error** → Input tidak sesuai format yang diharapkan  
""")
def create_book(
    data: BookRequest = Depends(BookRequest.as_form,),
    picture: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if picture.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only images are allowed")

    return book_service.create_book(db, data, picture)


@router.patch("/{book_id}",response_model=BookResponse,
             description="""
Endpoint untuk **mengupdate buku** berdasarkan ID buku.

- **book_id**: ID buku yang ingin diperbarui (path parameter)

- **title**: Judul buku (opsional)
- **author**: Nama penulis buku (opsional)
- **description**: Deskripsi singkat tentang buku (opsional)
- **picture**: Gambar buku (opsional)

Jika berhasil:
- **200 OK** → Mengembalikan data buku yang diperbarui

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
- **422 Validation Error** → Input tidak sesuai format yang diharapkan
""")
def update_book(
    book_id: int,
    data: BookRequest = Depends(BookUpdateRequest.as_form),
    picture: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if picture:  # hanya proses jika ada file valid
        if picture.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Only images are allowed")
    else:
        picture = None
    
    

    return book_service.update_book(db, data, book_id, picture)


@router.get("",
    summary="Get all Books",
    description="""
Mengambil daftar buku dengan dukungan **pagination**.  

Query parameter:
- **search** (str, optional) → Mencari pengguna berdasarkan username atau email
- **page** (int, default=1) → Halaman yang ingin ditampilkan  
- **per_page** (int, default=10) → Jumlah item per halaman  

Response:
- **200 OK** → Daftar pengguna beserta metadata pagination  
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
""",)
def get_book(
    request: Request,
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by title or author"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    return book_service.get_book(db, request, search, page, per_page)


@router.get("/{book_id}",
            response_model=ShowBookResponse,
            description="""
Endpoint untuk mengambil data buku.  

- **book_id** : ID buku yang ingin diambil. Jika tidak disertakan, akan mengembalikan daftar semua buku.  

Jika berhasil:
- **200 OK** → Mengembalikan data buku (atau daftar buku)  

Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
- **404 Not Found** → Buku dengan ID tersebut tidak ditemukan  
""")
def show_book(book_id: int, request: Request, db: Session = Depends(get_db)):
    return book_service.show_book(book_id, request, db)


@router.delete("/{book_id}", description="""
Endpoint untuk **menghapus buku** berdasarkan ID buku.  

- **book_id** (path parameter): ID buku yang ingin dihapus  

Jika berhasil:
- **200 OK** → Pesan konfirmasi bahwa buku berhasil dihapus  
Jika gagal:
- **401 Unauthorized** → Token tidak valid atau kedaluwarsa  
- **404 Not Found** → Buku dengan ID tersebut tidak ditemukan  
""",)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.delete_book(db, book_id)
