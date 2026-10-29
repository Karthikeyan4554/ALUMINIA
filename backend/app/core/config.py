import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_SQLITE_PATH = (BACKEND_DIR / "alumnia.db").as_posix()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Alumnia — AI-Powered Alumni Networking Platform"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "alumnia-super-secret-jwt-key-for-dev-2026-secure-random")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database configuration: defaults to SQLite for immediate local execution, seamlessly supports PostgreSQL / Supabase
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{DEFAULT_SQLITE_PATH}"
    )
    
    # Supabase credentials (optional for cloud integration)
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL", None)
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY", None)
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_ROLE_KEY", None)
    
    # LLM API configuration (supports OpenAI, Gemini, Groq, or Open-Source LLMs)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
