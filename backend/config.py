import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = Field(
        default="sqlite:///./sidemoney.db",
        env="DATABASE_URL",
        description="Database connection URL"
    )
    sql_echo: bool = Field(default=False, env="SQL_ECHO")
    
    # JWT
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY",
        description="JWT secret key"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30 * 24 * 60,  # 30 days
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    # Google OAuth
    google_client_id: str = Field(default="", env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(default="", env="GOOGLE_CLIENT_SECRET")
    
    # Google Generative AI (Gemini)
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-1.5-flash", env="GEMINI_MODEL")
    
    # CORS
    allowed_origins: List[str] = Field(
        default=["*"],
        env="ALLOWED_ORIGINS"
    )
    
    # Production
    environment: str = Field(default="development", env="ENVIRONMENT")
    allowed_hosts: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        env="ALLOWED_HOSTS"
    )
    port: int = Field(default=8000, env="PORT")
    
    # File uploads
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'allowed_hosts':
                return raw_val.split(',') if raw_val else []
            return raw_val


# Global settings instance
settings = Settings() 