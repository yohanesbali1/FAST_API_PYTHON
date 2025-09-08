from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI MySQL Project"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    JWT_ALGORITHM: str
    JWT_SECRET: str
    DB_NAME: str
    DATABASE_URL: str = ""   # inisialisasi kosong
    JWT_EXPIRE_MINUTES: int = 60     

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
