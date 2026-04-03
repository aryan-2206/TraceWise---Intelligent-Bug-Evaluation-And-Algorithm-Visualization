from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ]
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    
    # Execution settings
    CODE_TIMEOUT: int = 30  # seconds
    MAX_CODE_LENGTH: int = 10000  # characters
    
    # File paths
    SANDBOX_DIR: str = "sandbox"
    TEST_CASES_DIR: str = "test_cases"
    EXECUTION_LOGS_DIR: str = "sandbox/execution_logs"
    
    # Language settings
    SUPPORTED_LANGUAGES: List[str] = ["python", "javascript", "cpp"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.SANDBOX_DIR, exist_ok=True)
os.makedirs(settings.EXECUTION_LOGS_DIR, exist_ok=True)
os.makedirs(settings.TEST_CASES_DIR, exist_ok=True)
