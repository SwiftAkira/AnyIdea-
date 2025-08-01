"""
Database configuration and session management for AnyIdea? application.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
import logging
from contextlib import contextmanager
from typing import Generator

from app.models.database import Base
from config import settings

logger = logging.getLogger(__name__)

# Database URL
DATABASE_URL = f"sqlite:///{settings.database_path}"

# Create engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Allow multiple threads for SQLite
    poolclass=StaticPool,  # Use static pool for SQLite
    echo=settings.database_echo,  # Log SQL queries if enabled
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_tables():
    """Drop all database tables (use with caution!)."""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Use this in FastAPI endpoints as a dependency.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database session.
    Use this in service functions.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Database context error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_database():
    """Initialize the database with tables and any default data."""
    try:
        # Ensure database directory exists
        db_dir = os.path.dirname(settings.database_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Created database directory: {db_dir}")
        
        # Create tables
        create_tables()
        
        # Add any default data here if needed
        logger.info(f"Database initialized at: {settings.database_path}")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def check_database_health() -> dict:
    """Check database connection and return status."""
    try:
        with get_db_context() as db:
            # Simple query to test connection
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            
        return {
            "status": "healthy",
            "database_path": settings.database_path,
            "database_exists": os.path.exists(settings.database_path),
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database_path": settings.database_path,
            "database_exists": os.path.exists(settings.database_path),
            "error": str(e),
            "message": "Database connection failed"
        }
