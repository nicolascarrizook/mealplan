from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App
    app_name: str = "Meal Planner Pro"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # OpenAI
    openai_api_key: str
    
    # ChromaDB
    chromadb_host: str = "localhost"
    chromadb_port: int = 8001
    
    # CORS
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()