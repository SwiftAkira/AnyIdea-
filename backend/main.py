"""
Main FastAPI application for AnyIdea? backend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

from config import settings
from app.models.schemas import (
    SuggestionRequest, 
    SuggestionResponse, 
    ErrorResponse,
    ActivitySuggestion,
    WeatherInfo,
    AIMetadata
)
from app.services.openrouter_service import openrouter_service
from app.services.weather_service import weather_service

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
async def get_activity_suggestions(request: SuggestionRequest):
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
        
        # Get AI suggestions
        ai_response = await openrouter_service.get_activity_suggestions(
            budget=request.budget,
            time_available=request.time_available,
            location_data=location_data,
            weather_data=weather_data,
            preferences=preferences_data
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
        
        logger.info(f"Returning {len(suggestions)} suggestions")
        return response
        
    except Exception as e:
        logger.error(f"Error processing suggestion request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process suggestion request: {str(e)}"
        )


@app.get("/api/activities")
async def get_available_activities():
    """
    Get list of available activity types and categories.
    
    This endpoint returns metadata about available activity types, 
    energy levels, and other options for the frontend.
    """
    return {
        "activity_types": [
            "creative", "productive", "entertainment", 
            "exercise", "learning", "food", "social", 
            "outdoor", "indoor"
        ],
        "energy_levels": ["low", "medium", "high"],
        "social_levels": ["solo", "small_group", "large_group"],
        "skill_levels": ["beginner", "intermediate", "advanced"],
        "meal_types": ["snack", "breakfast", "lunch", "dinner", "dessert"],
        "time_units": ["minutes", "hours"]
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
            "places": settings.google_places_api_key != "",
            "yelp": settings.yelp_api_key != ""
        },
        "weather_configured": weather_service.is_available(),
        "message": "Location services ready"
    }


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
