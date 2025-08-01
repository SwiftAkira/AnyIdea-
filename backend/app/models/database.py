"""
Database models for AnyIdea? application.
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    """User model for storing user preferences and settings."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, unique=True, nullable=False)  # For anonymous users
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User preferences
    preferred_budget_min = Column(Float, default=0.0)
    preferred_budget_max = Column(Float, default=100.0)
    preferred_time_min = Column(Integer, default=30)  # minutes
    preferred_time_max = Column(Integer, default=120)  # minutes
    preferred_location = Column(String, default="either")  # indoor/outdoor/either
    preferred_energy_level = Column(String, default="medium")
    preferred_social_level = Column(String, default="solo")
    
    # Location data (if user allows)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    allow_location_access = Column(Boolean, default=False)
    
    # Relationships
    custom_categories = relationship("CustomCategory", back_populates="user", cascade="all, delete-orphan")
    activity_history = relationship("ActivityHistory", back_populates="user", cascade="all, delete-orphan")


class CustomCategory(Base):
    """Custom activity categories created by users."""
    __tablename__ = "custom_categories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(String(100), nullable=False)  # normalized ID for API use
    icon = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="custom_categories")
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.category_id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "type": "custom",
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ActivitySuggestionLog(Base):
    """Log of activity suggestions made by the system."""
    __tablename__ = "activity_suggestion_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # Can be anonymous
    session_id = Column(String, nullable=False)  # Track anonymous sessions
    request_id = Column(String, nullable=False)  # Link to API request
    
    # Request parameters
    budget = Column(Float, nullable=False)
    time_available = Column(Integer, nullable=False)
    location_preference = Column(String, nullable=True)
    energy_level = Column(String, nullable=True)
    activity_types = Column(JSON, nullable=True)  # List of selected types
    custom_categories = Column(JSON, nullable=True)  # List of custom categories used
    mood = Column(String, nullable=True)
    
    # Weather data at time of request
    weather_data = Column(JSON, nullable=True)
    
    # AI response metadata
    ai_model_used = Column(String, nullable=True)
    ai_reasoning = Column(Text, nullable=True)
    processing_time = Column(Float, nullable=True)
    suggestions_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    suggestions = relationship("ActivitySuggestionItem", back_populates="suggestion_log", cascade="all, delete-orphan")


class ActivitySuggestionItem(Base):
    """Individual activity suggestions within a suggestion log."""
    __tablename__ = "activity_suggestion_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    suggestion_log_id = Column(String, ForeignKey("activity_suggestion_logs.id"), nullable=False)
    
    # Activity details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)  # ai_generated, local_business, etc.
    time_required = Column(Integer, nullable=False)  # minutes
    cost = Column(Float, nullable=False)
    difficulty = Column(String(20), nullable=False)
    
    # Additional metadata
    instructions = Column(JSON, nullable=True)  # List of instruction steps
    materials_needed = Column(JSON, nullable=True)  # List of required materials
    address = Column(String(500), nullable=True)
    distance = Column(String(50), nullable=True)
    rating = Column(Float, nullable=True)
    hours = Column(String(200), nullable=True)
    weather_appropriate = Column(Boolean, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    suggestion_log = relationship("ActivitySuggestionLog", back_populates="suggestions")


class ActivityHistory(Base):
    """Track which activities users have selected or completed."""
    __tablename__ = "activity_history"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    suggestion_item_id = Column(String, ForeignKey("activity_suggestion_items.id"), nullable=True)
    
    # Activity details (in case suggestion is deleted)
    activity_title = Column(String(200), nullable=False)
    activity_type = Column(String(50), nullable=False)
    activity_cost = Column(Float, nullable=False)
    activity_time = Column(Integer, nullable=False)
    
    # User feedback
    selected = Column(Boolean, default=False)  # User clicked/selected this activity
    completed = Column(Boolean, default=False)  # User marked as completed
    rating = Column(Integer, nullable=True)  # 1-5 star rating
    feedback = Column(Text, nullable=True)  # User comments
    
    # Timestamps
    selected_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="activity_history")
    suggestion_item = relationship("ActivitySuggestionItem")


class PopularActivity(Base):
    """Track popular activities for recommendations."""
    __tablename__ = "popular_activities"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    activity_title = Column(String(200), nullable=False)
    activity_type = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    
    # Popularity metrics
    selection_count = Column(Integer, default=0)
    completion_count = Column(Integer, default=0)
    average_rating = Column(Float, nullable=True)
    total_ratings = Column(Integer, default=0)
    
    # Budget and time ranges where this activity is popular
    popular_budget_min = Column(Float, nullable=True)
    popular_budget_max = Column(Float, nullable=True)
    popular_time_min = Column(Integer, nullable=True)
    popular_time_max = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
