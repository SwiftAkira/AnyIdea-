"""
Database service for managing custom categories and user data.
"""
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime

from app.models.database import (
    User, CustomCategory, ActivitySuggestionLog, 
    ActivitySuggestionItem, ActivityHistory, PopularActivity
)
from app.database import get_db_context

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations."""
    
    @staticmethod
    def get_or_create_user(session_id: str, db: Session) -> User:
        """Get existing user by session ID or create a new one."""
        user = db.query(User).filter(User.session_id == session_id).first()
        if not user:
            user = User(session_id=session_id)
            db.add(user)
            db.commit()  # Commit the new user
            logger.info(f"Created new user with session_id: {session_id}")
        return user
    
    @staticmethod
    def create_custom_category(
        session_id: str,
        category_name: str,
        description: Optional[str] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """Create a new custom category for a user."""
        if db is None:
            with get_db_context() as db:
                return DatabaseService.create_custom_category(session_id, category_name, description, db)
        
        try:
            # Get or create user
            user = DatabaseService.get_or_create_user(session_id, db)
            
            # Generate category ID
            category_id = category_name.lower().replace(" ", "_").replace("&", "and")
            
            # Check if category already exists for this user
            existing = db.query(CustomCategory).filter(
                and_(
                    CustomCategory.user_id == user.id,
                    CustomCategory.category_id == category_id,
                    CustomCategory.is_active == True
                )
            ).first()
            
            if existing:
                logger.info(f"Custom category '{category_name}' already exists for user {session_id}")
                return {
                    "status": "duplicate",
                    "message": f"You already have a category named '{category_name}'",
                    "accepted": False,
                    "existing_category": existing.to_dict()
                }
            
            # Create new category
            custom_category = CustomCategory(
                user_id=user.id,
                name=category_name.strip().title(),
                description=description,
                category_id=category_id
            )
            
            db.add(custom_category)
            db.commit()  # Commit the new category
            
            logger.info(f"Created custom category '{category_name}' for user {session_id}")
            
            return {
                "status": "accepted",
                "message": f"Custom category '{custom_category.name}' has been created successfully",
                "accepted": True,
                "category": custom_category.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error creating custom category: {e}")
            raise
    
    @staticmethod
    def get_user_custom_categories(session_id: str, db: Session = None) -> List[Dict[str, Any]]:
        """Get all active custom categories for a user."""
        if db is None:
            with get_db_context() as db:
                return DatabaseService.get_user_custom_categories(session_id, db)
        
        try:
            user = db.query(User).filter(User.session_id == session_id).first()
            if not user:
                return []
            
            categories = db.query(CustomCategory).filter(
                and_(
                    CustomCategory.user_id == user.id,
                    CustomCategory.is_active == True
                )
            ).order_by(CustomCategory.created_at.desc()).all()
            
            return [cat.to_dict() for cat in categories]
            
        except Exception as e:
            logger.error(f"Error getting user custom categories: {e}")
            return []
    
    @staticmethod
    def deactivate_custom_category(session_id: str, category_id: str, db: Session = None) -> bool:
        """Deactivate (soft delete) a custom category."""
        if db is None:
            with get_db_context() as db:
                return DatabaseService.deactivate_custom_category(session_id, category_id, db)
        
        try:
            user = db.query(User).filter(User.session_id == session_id).first()
            if not user:
                return False
            
            category = db.query(CustomCategory).filter(
                and_(
                    CustomCategory.user_id == user.id,
                    CustomCategory.category_id == category_id,
                    CustomCategory.is_active == True
                )
            ).first()
            
            if category:
                category.is_active = False
                category.updated_at = datetime.utcnow()
                logger.info(f"Deactivated custom category '{category.name}' for user {session_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deactivating custom category: {e}")
            return False
    
    @staticmethod
    def log_activity_suggestion(
        session_id: str,
        request_data: Dict[str, Any],
        suggestions: List[Dict[str, Any]],
        ai_metadata: Dict[str, Any],
        request_id: str,
        db: Session = None
    ) -> str:
        """Log an activity suggestion request and response."""
        if db is None:
            with get_db_context() as db:
                return DatabaseService.log_activity_suggestion(
                    session_id, request_data, suggestions, ai_metadata, request_id, db
                )
        
        try:
            # Get or create user
            user = DatabaseService.get_or_create_user(session_id, db)
            
            # Create suggestion log
            suggestion_log = ActivitySuggestionLog(
                user_id=user.id,
                session_id=session_id,
                request_id=request_id,
                budget=request_data.get("budget", 0),
                time_available=request_data.get("time_available", 0),
                location_preference=request_data.get("location_preference"),
                energy_level=request_data.get("energy_level"),
                activity_types=request_data.get("activity_types", []),
                custom_categories=request_data.get("custom_categories", []),
                mood=request_data.get("mood"),
                weather_data=request_data.get("weather_data"),
                ai_model_used=ai_metadata.get("model_used"),
                ai_reasoning=ai_metadata.get("reasoning"),
                processing_time=ai_metadata.get("processing_time"),
                suggestions_count=len(suggestions)
            )
            
            db.add(suggestion_log)
            db.flush()  # Get the ID
            
            # Create suggestion items
            for suggestion in suggestions:
                suggestion_item = ActivitySuggestionItem(
                    suggestion_log_id=suggestion_log.id,
                    title=suggestion.get("title", ""),
                    description=suggestion.get("description", ""),
                    type=suggestion.get("type", ""),
                    time_required=suggestion.get("time_required", 0),
                    cost=suggestion.get("cost", 0.0),
                    difficulty=suggestion.get("difficulty", "easy"),
                    instructions=suggestion.get("instructions", []),
                    materials_needed=suggestion.get("materials_needed", []),
                    address=suggestion.get("address"),
                    distance=suggestion.get("distance"),
                    rating=suggestion.get("rating"),
                    hours=suggestion.get("hours"),
                    weather_appropriate=suggestion.get("weather_appropriate")
                )
                db.add(suggestion_item)
            
            logger.info(f"Logged activity suggestion for user {session_id}: {len(suggestions)} suggestions")
            return suggestion_log.id
            
        except Exception as e:
            logger.error(f"Error logging activity suggestion: {e}")
            raise
    
    @staticmethod
    def get_user_activity_history(session_id: str, limit: int = 10, db: Session = None) -> List[Dict[str, Any]]:
        """Get user's recent activity history."""
        if db is None:
            with get_db_context() as db:
                return DatabaseService.get_user_activity_history(session_id, limit, db)
        
        try:
            user = db.query(User).filter(User.session_id == session_id).first()
            if not user:
                return []
            
            logs = db.query(ActivitySuggestionLog).filter(
                ActivitySuggestionLog.user_id == user.id
            ).order_by(ActivitySuggestionLog.created_at.desc()).limit(limit).all()
            
            history = []
            for log in logs:
                history.append({
                    "request_id": log.request_id,
                    "budget": log.budget,
                    "time_available": log.time_available,
                    "suggestions_count": log.suggestions_count,
                    "ai_model_used": log.ai_model_used,
                    "created_at": log.created_at.isoformat() if log.created_at else None
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting user activity history: {e}")
            return []
    
    @staticmethod
    def get_popular_activities(
        budget_range: Optional[tuple] = None,
        time_range: Optional[tuple] = None,
        limit: int = 10,
        db: Session = None
    ) -> List[Dict[str, Any]]:
        """Get popular activities based on user selections and ratings."""
        if db is None:
            with get_db_context() as db:
                return DatabaseService.get_popular_activities(budget_range, time_range, limit, db)
        
        try:
            query = db.query(PopularActivity).filter(PopularActivity.selection_count > 0)
            
            # Apply filters
            if budget_range:
                min_budget, max_budget = budget_range
                query = query.filter(
                    and_(
                        PopularActivity.popular_budget_min <= max_budget,
                        PopularActivity.popular_budget_max >= min_budget
                    )
                )
            
            if time_range:
                min_time, max_time = time_range
                query = query.filter(
                    and_(
                        PopularActivity.popular_time_min <= max_time,
                        PopularActivity.popular_time_max >= min_time
                    )
                )
            
            activities = query.order_by(
                PopularActivity.selection_count.desc(),
                PopularActivity.average_rating.desc()
            ).limit(limit).all()
            
            return [
                {
                    "title": activity.activity_title,
                    "type": activity.activity_type,
                    "category": activity.category,
                    "selection_count": activity.selection_count,
                    "completion_count": activity.completion_count,
                    "average_rating": activity.average_rating,
                    "total_ratings": activity.total_ratings
                }
                for activity in activities
            ]
            
        except Exception as e:
            logger.error(f"Error getting popular activities: {e}")
            return []


# Global service instance
database_service = DatabaseService()
