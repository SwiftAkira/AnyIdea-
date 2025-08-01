"""
Configuration settings for the AnyIdea backend API.
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Database
    database_url: str = Field(default="sqlite:///./anyidea.db", env="DATABASE_URL")
    database_path: str = Field(default="./data/anyidea.db", env="DATABASE_PATH")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")  # Log SQL queries
    
    # API Keys
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    weather_api_key: str = Field(default="", env="WEATHER_API_KEY")
    google_places_api_key: str = Field(default="", env="GOOGLE_PLACES_API_KEY")
    yelp_api_key: str = Field(default="", env="YELP_API_KEY")
    
    # API Configuration
    api_host: str = Field(default="localhost", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_reload: bool = Field(default=True, env="API_RELOAD")
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000", 
            "http://localhost:5173"
        ],
        env="ALLOWED_ORIGINS"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
