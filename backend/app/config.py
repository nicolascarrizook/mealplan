from pydantic_settings import BaseSettings
from typing import List
import os
import json

class Settings(BaseSettings):
    # App
    app_name: str = "Meal Planner Pro"
    app_version: str = "1.0.0"
    debug: bool = False  # Default to False for production
    
    # OpenAI
    openai_api_key: str
    
    # ChromaDB
    chromadb_host: str = "chromadb"  # Docker service name
    chromadb_port: int = 8000
    
    # CORS - will be loaded from environment
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    def __init__(self, **values):
        super().__init__(**values)
        # Parse BACKEND_CORS_ORIGINS if it's a string
        cors_origins = os.getenv("BACKEND_CORS_ORIGINS")
        if cors_origins:
            try:
                self.backend_cors_origins = json.loads(cors_origins)
            except json.JSONDecodeError:
                # If it's not valid JSON, treat it as a comma-separated list
                self.backend_cors_origins = [origin.strip() for origin in cors_origins.split(",")]

settings = Settings()