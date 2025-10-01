import os
from typing import Literal

class Settings:
    """Application configuration settings"""
    
    # Storage configuration
    STORAGE_TYPE: Literal["file", "mongodb"] = os.getenv("STORAGE_TYPE", "file")
    
    # MongoDB configuration
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "maps_db")
    
    # File storage configuration
    STORAGE_FILE: str = os.getenv("STORAGE_FILE", "maps_data.json")
    
    # Image proxy configuration
    IMAGE_CACHE_DIR: str = os.getenv("IMAGE_CACHE_DIR", "image_cache")
    
    # API configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

settings = Settings()