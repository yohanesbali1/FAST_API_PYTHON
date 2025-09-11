# 🚀 Simple FastAPI Project with JWT Authentication & Custom Error Handling

Project sederhana menggunakan **FastAPI** dengan fitur:

- 🔐 **JWT Authentication** → untuk autentikasi aman
- ⚠️ **Custom Global Error Responses** → untuk konsistensi format error
- 📖 **API Documentation** otomatis dengan Swagger & ReDoc

Database yang digunakan: **MySQL**

---

## 📦 Cara Menggunakan

### 1️⃣ Clone Project

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2️⃣ Install Dependencies

Disarankan menggunakan virtual environment (`venv` atau `conda`)

```bash
pip install -r requirements.txt
```

### 3️⃣ Migrasi Database

Jalankan Alembic untuk memastikan struktur database terbaru:

```bash
alembic upgrade head
```

### 4️⃣ Jalankan Seeder

Untuk mengisi data awal (opsional, jika tersedia):

```bash
python app/seed.py
```

### 5️⃣ Jalankan FastAPI

```bash
uvicorn app.main:app --reload
```

---

## 📑 Dokumentasi API

Setelah server berjalan, dokumentasi API tersedia di:

- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠️ Teknologi yang Digunakan

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [JWT (PyJWT)](https://pyjwt.readthedocs.io/en/stable/)
- [Pydantic](https://docs.pydantic.dev/)

---

## 📌 Fitur Utama

- Registrasi & Login dengan JWT
- Custom Response untuk Error (422, 401, 403, 500, dll.)
- Menggunakan MySQL sebagai database utama
- Struktur project modular & clean

---

## 🔑 Contoh Endpoint

### Register

**POST** `/register`

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "secret123"
}
```

### Login

**POST** `/login`

```json
{
  "username": "user1",
  "password": "secret123"
}
```

**Response**

```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer"
}
```

### Profile (Protected)

**GET** `/profile`  
Headers:

```
Authorization: Bearer <access_token>
```

**Response**

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com"
}
```

---

## ⚠️ Custom Error Response

Format konsisten:

```json
{
  "errors": "Username field required [+1 more] "
}
```

---

## 📄 License

MIT License – bebas digunakan & dikembangkan.
