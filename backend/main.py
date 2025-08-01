"""
Main FastAPI application for AnyIdea? backend.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from config import settings
from app.models.schemas import (
    SuggestionRequest, 
    SuggestionResponse, 
    ErrorResponse,
    ActivitySuggestion,
    WeatherInfo,
    AIMetadata,
    ActivitiesResponse,
    ActivityCategory,
    CustomActivityRequest
)
from app.services.openrouter_service import openrouter_service
from app.services.weather_service import weather_service
from app.services.database_service import database_service
from app.services.places_service import places_service
from app.database import get_db, init_database, check_database_health

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AnyIdea? API",
    description="Activity suggestion API that helps you figure out what to do when you're bored",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting AnyIdea? API server...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Log level: {settings.log_level}")
    
    # Initialize database
    try:
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down AnyIdea? API server...")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.environment == "development" else None,
            error_code="INTERNAL_ERROR",
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AnyIdea? API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment
    }


@app.post("/api/suggest", response_model=SuggestionResponse)
async def get_activity_suggestions(
    request: SuggestionRequest,
    session_id: str = "anonymous",
    db: Session = Depends(get_db)
):
    """
    Get personalized activity suggestions based on user preferences.
    
    This endpoint takes user input including budget, time, location, and preferences,
    then returns a list of personalized activity suggestions.
    """
    try:
        logger.info(f"Received suggestion request: budget={request.budget}, time={request.time_available}")
        
        # Get weather data if location is provided
        weather_data = None
        if request.location and request.location.allow_location_access:
            weather_data = await weather_service.get_current_weather(
                request.location.latitude,
                request.location.longitude
            )
            logger.info(f"Weather data retrieved: {weather_data['current'] if weather_data else 'None'}")
        
        # Prepare data for AI service
        location_data = None
        if request.location:
            location_data = {
                "latitude": request.location.latitude,
                "longitude": request.location.longitude,
                "allow_location_access": request.location.allow_location_access
            }
        
        preferences_data = {
            "location": request.activity_preferences.location,
            "social_level": request.activity_preferences.social_level,
            "activity_types": request.activity_preferences.activity_types,
            "energy_level": request.activity_preferences.energy_level,
            "mood": request.activity_preferences.mood
        }
        
        # Extract custom categories
        custom_categories = request.activity_preferences.custom_categories if request.activity_preferences.custom_categories else None
        
        # Get AI suggestions
        ai_response = await openrouter_service.get_activity_suggestions(
            budget=request.budget,
            time_available=request.time_available,
            location_data=location_data,
            weather_data=weather_data,
            preferences=preferences_data,
            custom_categories=custom_categories
        )
        
        # Convert AI suggestions to our format
        suggestions = []
        for ai_suggestion in ai_response.get("suggestions", []):
            suggestion = ActivitySuggestion(
                type="ai_generated" if ai_response.get("success") else "fallback",
                title=ai_suggestion.get("title", "Activity"),
                description=ai_suggestion.get("description", ""),
                time_required=ai_suggestion.get("time_required", request.time_available),
                cost=ai_suggestion.get("cost", 0.0),
                difficulty=ai_suggestion.get("difficulty", "easy"),
                instructions=ai_suggestion.get("instructions", []),
                materials_needed=ai_suggestion.get("materials_needed", []),
                ai_reasoning=ai_response.get("reasoning")
            )
            suggestions.append(suggestion)
        
        # Add location-based venue suggestions if location is provided
        if location_data and location_data.get("allow_location_access") and places_service.is_available():
            try:
                # Determine budget level from request
                budget_level = "moderate"
                if request.budget <= 0:
                    budget_level = "free"
                elif request.budget <= 20:
                    budget_level = "low"
                elif request.budget <= 50:
                    budget_level = "moderate"
                else:
                    budget_level = "high"
                
                # Get venue suggestions for different activity types
                venue_types = []
                if request.activity_preferences and request.activity_preferences.activity_types:
                    activity_type_mapping = {
                        "entertainment": "entertainment",
                        "exercise": "exercise", 
                        "food": "food",
                        "productive": "learning",
                        "creative": "culture",
                        "learning": "learning",
                        "social": "entertainment"
                    }
                    
                    for activity_type in request.activity_preferences.activity_types:
                        mapped_type = activity_type_mapping.get(str(activity_type).lower())
                        if mapped_type and mapped_type not in venue_types:
                            venue_types.append(mapped_type)
                
                # Default to food and entertainment if no specific types
                if not venue_types:
                    venue_types = ["food", "entertainment"]
                
                # Get venues for each activity type
                for venue_type in venue_types[:2]:  # Limit to 2 types to avoid too many suggestions
                    venues = await places_service.get_activity_venues(
                        latitude=location_data["latitude"],
                        longitude=location_data["longitude"],
                        activity_type=venue_type,
                        budget_level=budget_level,
                        radius=5000
                    )
                    
                    # Convert venues to suggestions
                    for venue in venues[:3]:  # Limit to 3 venues per type
                        location_suggestion = ActivitySuggestion(
                            type="location_based",
                            title=f"Visit {venue.get('name', 'Local Venue')}",
                            description=f"Check out this {venue_type} venue nearby: {venue.get('vicinity', 'Local area')}",
                            time_required=request.time_available,
                            cost=venue.get("price_level", 0) * 15.0,  # Rough cost estimate
                            difficulty="easy",
                            instructions=[f"Head to {venue.get('name')}", "Enjoy your visit!"],
                            materials_needed=[],
                            address=venue.get("vicinity"),
                            rating=venue.get("rating"),
                            hours=venue.get("opening_hours", {}),
                            distance=None  # Could calculate if needed
                        )
                        suggestions.append(location_suggestion)
                
                logger.info(f"Added {len([s for s in suggestions if s.type == 'location_based'])} location-based suggestions")
                
            except Exception as e:
                logger.warning(f"Failed to get location-based suggestions: {e}")
                # Don't fail the whole request if location services fail
        
        # Create weather info
        weather_info = None
        if weather_data:
            weather_info = WeatherInfo(
                current=weather_data["current"],
                suitable_for_outdoor=weather_data["suitable_for_outdoor"],
                temperature=weather_data.get("temperature"),
                humidity=weather_data.get("humidity")
            )
        
        # Create AI metadata
        ai_metadata = AIMetadata(
            model_used=ai_response.get("model_used", "unknown"),
            reasoning=ai_response.get("reasoning", ""),
            processing_time=ai_response.get("processing_time", 0.0)
        )
        
        response = SuggestionResponse(
            suggestions=suggestions,
            weather=weather_info,
            ai_metadata=ai_metadata,
            total_suggestions=len(suggestions),
            request_id=f"req_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        )
        
        # Log the suggestion to database
        try:
            request_data = {
                "budget": request.budget,
                "time_available": request.time_available,
                "location_preference": request.activity_preferences.location if request.activity_preferences else None,
                "energy_level": request.activity_preferences.energy_level if request.activity_preferences else None,
                "activity_types": [str(at) for at in request.activity_preferences.activity_types] if request.activity_preferences else [],
                "custom_categories": request.activity_preferences.custom_categories if request.activity_preferences else [],
                "mood": request.activity_preferences.mood if request.activity_preferences else None,
                "weather_data": weather_data
            }
            
            suggestions_data = [
                {
                    "title": s.title,
                    "description": s.description,
                    "type": s.type,
                    "time_required": s.time_required,
                    "cost": s.cost,
                    "difficulty": s.difficulty,
                    "instructions": s.instructions,
                    "materials_needed": s.materials_needed,
                    "address": s.address,
                    "distance": s.distance,
                    "rating": s.rating,
                    "hours": s.hours,
                    "weather_appropriate": s.weather_appropriate
                }
                for s in suggestions
            ]
            
            ai_metadata_dict = {
                "model_used": ai_metadata.model_used,
                "reasoning": ai_metadata.reasoning,
                "processing_time": ai_metadata.processing_time
            }
            
            database_service.log_activity_suggestion(
                session_id=session_id,
                request_data=request_data,
                suggestions=suggestions_data,
                ai_metadata=ai_metadata_dict,
                request_id=response.request_id,
                db=db
            )
            logger.info(f"Logged activity suggestion to database: {response.request_id}")
            
        except Exception as e:
            logger.warning(f"Failed to log suggestion to database: {e}")
            # Don't fail the request if logging fails
        
        logger.info(f"Returning {len(suggestions)} suggestions")
        return response
        
    except Exception as e:
        logger.error(f"Error processing suggestion request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process suggestion request: {str(e)}"
        )


@app.get("/api/activities", response_model=ActivitiesResponse)
async def get_available_activities():
    """
    Get list of available activity types, categories, and options.
    
    This endpoint returns comprehensive metadata about available activity categories,
    types, energy levels, and other options for the frontend. It also supports
    information about custom categories that users can input.
    """
    try:
        # Define predefined activity categories with rich metadata
        predefined_categories = [
            ActivityCategory(
                id="creative",
                name="Creative & Arts",
                description="Artistic and creative activities to express yourself",
                icon="palette",
                examples=["Drawing", "Painting", "Writing", "Crafting", "Photography", "Music"]
            ),
            ActivityCategory(
                id="productive",
                name="Productive & Useful",
                description="Tasks that help you accomplish goals or improve your life",
                icon="checkmark",
                examples=["Organizing", "Cleaning", "Planning", "Reading", "Skill Building", "Home Improvement"]
            ),
            ActivityCategory(
                id="entertainment",
                name="Entertainment & Fun",
                description="Activities for relaxation and enjoyment",
                icon="play",
                examples=["Movies", "TV Shows", "Games", "Puzzles", "YouTube", "Podcasts"]
            ),
            ActivityCategory(
                id="exercise",
                name="Exercise & Fitness",
                description="Physical activities to stay active and healthy",
                icon="fitness",
                examples=["Walking", "Running", "Yoga", "Home Workouts", "Dancing", "Sports"]
            ),
            ActivityCategory(
                id="learning",
                name="Learning & Education",
                description="Activities to expand your knowledge and skills",
                icon="book",
                examples=["Online Courses", "Language Learning", "Tutorials", "Research", "Reading", "Practice"]
            ),
            ActivityCategory(
                id="food",
                name="Food & Cooking",
                description="Culinary activities and food-related experiences",
                icon="restaurant",
                examples=["Cooking", "Baking", "Food Delivery", "Recipes", "Meal Prep", "Food Exploration"]
            ),
            ActivityCategory(
                id="social",
                name="Social & Connection",
                description="Activities involving interaction with others",
                icon="people",
                examples=["Video Calls", "Messaging", "Online Gaming", "Social Media", "Community Events"]
            ),
            ActivityCategory(
                id="outdoor",
                name="Outdoor Adventures",
                description="Activities that take you outside and into nature",
                icon="sunny",
                examples=["Hiking", "Gardening", "Photography", "Sports", "Walking", "Picnics"]
            ),
            ActivityCategory(
                id="indoor",
                name="Indoor Comfort",
                description="Cozy activities you can enjoy from the comfort of home",
                icon="home",
                examples=["Reading", "Gaming", "Cooking", "Movies", "Crafts", "Organizing"]
            ),
            ActivityCategory(
                id="relaxation",
                name="Rest & Relaxation",
                description="Activities to unwind and recharge your mind and body",
                icon="leaf",
                examples=["Meditation", "Bath", "Napping", "Breathing Exercises", "Stretching", "Journaling"]
            )
        ]
        
        # Activity types with descriptions
        activity_types = [
            {"value": "creative", "label": "Creative & Arts", "description": "Express your creativity"},
            {"value": "productive", "label": "Productive", "description": "Get things done"},
            {"value": "entertainment", "label": "Entertainment", "description": "Have fun and relax"},
            {"value": "exercise", "label": "Exercise", "description": "Stay active and healthy"},
            {"value": "learning", "label": "Learning", "description": "Expand your knowledge"},
            {"value": "food", "label": "Food & Cooking", "description": "Culinary experiences"},
            {"value": "social", "label": "Social", "description": "Connect with others"},
            {"value": "outdoor", "label": "Outdoor", "description": "Enjoy the outdoors"},
            {"value": "indoor", "label": "Indoor", "description": "Stay comfortable inside"}
        ]
        
        # Energy levels with descriptions
        energy_levels = [
            {"value": "low", "label": "Low Energy", "description": "Relaxing, minimal effort activities"},
            {"value": "medium", "label": "Medium Energy", "description": "Moderate effort, engaging activities"},
            {"value": "high", "label": "High Energy", "description": "Active, energetic activities"}
        ]
        
        # Social levels with descriptions
        social_levels = [
            {"value": "solo", "label": "Solo", "description": "Activities you can do alone"},
            {"value": "small_group", "label": "Small Group", "description": "Activities with a few friends"},
            {"value": "large_group", "label": "Large Group", "description": "Activities with many people"}
        ]
        
        # Skill levels with descriptions
        skill_levels = [
            {"value": "beginner", "label": "Beginner", "description": "No experience required"},
            {"value": "intermediate", "label": "Intermediate", "description": "Some experience helpful"},
            {"value": "advanced", "label": "Advanced", "description": "Significant experience required"}
        ]
        
        response = ActivitiesResponse(
            predefined_categories=predefined_categories,
            activity_types=activity_types,
            energy_levels=energy_levels,
            social_levels=social_levels,
            skill_levels=skill_levels,
            supports_custom_categories=True
        )
        
        logger.info(f"Returning {len(predefined_categories)} predefined categories and metadata")
        return response
        
    except Exception as e:
        logger.error(f"Error getting activities: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve activities: {str(e)}"
        )


@app.post("/api/activities/custom")
async def create_custom_activity_category(
    request: CustomActivityRequest,
    session_id: str = "anonymous",  # In real app, get from session/cookies
    db: Session = Depends(get_db)
):
    """
    Accept and validate a custom activity category from the user.
    
    This endpoint allows users to input their own activity categories
    that aren't covered by the predefined options. The custom category
    is stored in the database and can be used in future suggestions.
    """
    try:
        logger.info(f"Received custom activity category: {request.category_name}")
        
        # Validate and sanitize the custom category
        category_name = request.category_name.strip().title()
        
        # Check if it's too similar to existing predefined categories
        predefined_names = [
            "creative", "productive", "entertainment", "exercise", 
            "learning", "food", "social", "outdoor", "indoor", "relaxation"
        ]
        
        if category_name.lower() in [name.lower() for name in predefined_names]:
            return {
                "status": "duplicate",
                "message": f"'{category_name}' is already available as a predefined category",
                "suggestion": "Please choose from predefined categories or use a more specific name",
                "accepted": False
            }
        
        # Create custom category in database
        result = database_service.create_custom_category(
            session_id=session_id,
            category_name=category_name,
            description=request.description,
            db=db
        )
        
        if result["accepted"]:
            logger.info(f"Accepted custom category: {result['category']}")
        
        return {
            **result,
            "usage_instructions": "You can now use this category in your activity preferences"
        }
        
    except Exception as e:
        logger.error(f"Error processing custom category: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process custom category: {str(e)}"
        )


@app.get("/api/activities/custom")
async def get_user_custom_categories(
    session_id: str = "anonymous",
    db: Session = Depends(get_db)
):
    """
    Get all custom categories created by the user.
    
    This endpoint returns all active custom categories that the user
    has created, which can be used in activity suggestions.
    """
    try:
        custom_categories = database_service.get_user_custom_categories(session_id, db)
        
        return {
            "custom_categories": custom_categories,
            "count": len(custom_categories),
            "message": f"Found {len(custom_categories)} custom categories"
        }
        
    except Exception as e:
        logger.error(f"Error getting user custom categories: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get custom categories: {str(e)}"
        )


@app.delete("/api/activities/custom/{category_id}")
async def delete_custom_category(
    category_id: str,
    session_id: str = "anonymous",
    db: Session = Depends(get_db)
):
    """
    Delete (deactivate) a custom category.
    
    This endpoint soft-deletes a custom category by marking it as inactive.
    """
    try:
        success = database_service.deactivate_custom_category(session_id, category_id, db)
        
        if success:
            return {
                "status": "deleted",
                "message": f"Custom category '{category_id}' has been deleted",
                "success": True
            }
        else:
            return {
                "status": "not_found",
                "message": f"Custom category '{category_id}' not found or already deleted",
                "success": False
            }
        
    except Exception as e:
        logger.error(f"Error deleting custom category: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete custom category: {str(e)}"
        )


@app.get("/api/user/history")
async def get_user_history(
    session_id: str = "anonymous",
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get user's activity suggestion history.
    
    This endpoint returns the user's recent activity suggestion requests
    and can be used to show past preferences or suggest similar activities.
    """
    try:
        history = database_service.get_user_activity_history(session_id, limit, db)
        
        return {
            "history": history,
            "count": len(history),
            "limit": limit,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Error getting user history: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get user history: {str(e)}"
        )


@app.get("/api/activities/popular")
async def get_popular_activities(
    budget_min: float = None,
    budget_max: float = None,
    time_min: int = None,
    time_max: int = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get popular activities based on user selections and ratings.
    
    This endpoint returns activities that are frequently selected by users,
    optionally filtered by budget and time constraints.
    """
    try:
        budget_range = None
        if budget_min is not None and budget_max is not None:
            budget_range = (budget_min, budget_max)
        
        time_range = None
        if time_min is not None and time_max is not None:
            time_range = (time_min, time_max)
        
        popular_activities = database_service.get_popular_activities(
            budget_range=budget_range,
            time_range=time_range,
            limit=limit,
            db=db
        )
        
        return {
            "popular_activities": popular_activities,
            "count": len(popular_activities),
            "filters": {
                "budget_range": budget_range,
                "time_range": time_range,
                "limit": limit
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting popular activities: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get popular activities: {str(e)}"
        )


@app.get("/api/database/health")
async def get_database_health():
    """
    Check database connection and status.
    
    This endpoint provides information about database connectivity
    and can be used for health monitoring.
    """
    try:
        health_status = check_database_health()
        return health_status
        
    except Exception as e:
        logger.error(f"Error checking database health: {e}")
        return {
            "status": "error",
            "message": f"Failed to check database health: {str(e)}"
        }


@app.get("/api/location")
async def get_location_services():
    """
    Get location-based services status and information.
    
    This endpoint provides information about location services
    and can be used to test location-based features.
    """
    return {
        "status": "available",
        "services": {
            "weather": weather_service.is_available(),
            "places": places_service.is_available(),
            "yelp": settings.yelp_api_key != ""
        },
        "weather_configured": weather_service.is_available(),
        "places_configured": places_service.is_available(),
        "message": "Location services ready"
    }


@app.get("/api/location/nearby")
async def get_nearby_venues(
    latitude: float,
    longitude: float,
    activity_type: str = "food",
    budget_level: str = "moderate",
    radius: int = 5000
):
    """
    Get nearby venues for testing the Places API integration.
    
    This endpoint allows direct testing of the Google Places integration
    for debugging and development purposes.
    """
    try:
        if not places_service.is_available():
            raise HTTPException(
                status_code=503,
                detail="Google Places API not configured"
            )
        
        venues = await places_service.get_activity_venues(
            latitude=latitude,
            longitude=longitude,
            activity_type=activity_type,
            budget_level=budget_level,
            radius=radius
        )
        
        return {
            "venues": venues,
            "count": len(venues),
            "search_params": {
                "latitude": latitude,
                "longitude": longitude,
                "activity_type": activity_type,
                "budget_level": budget_level,
                "radius": radius
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting nearby venues: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get nearby venues: {str(e)}"
        )


@app.get("/api/ai-suggest")
async def get_ai_suggestion_status():
    """
    Get AI suggestion service status.
    
    This endpoint provides information about AI service availability.
    """
    is_available = openrouter_service.is_available()
    return {
        "status": "available" if is_available else "not_configured",
        "model": "moonshotai/kimi-k2:free",
        "openrouter_configured": is_available,
        "message": "AI suggestion service ready" if is_available else "OpenRouter API key not configured"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
