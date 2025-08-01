"""
Pydantic models for request/response data validation.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ActivityType(str, Enum):
    """Types of activities."""
    CREATIVE = "creative"
    PRODUCTIVE = "productive"
    ENTERTAINMENT = "entertainment"
    EXERCISE = "exercise"
    LEARNING = "learning"
    FOOD = "food"
    SOCIAL = "social"
    OUTDOOR = "outdoor"
    INDOOR = "indoor"


class EnergyLevel(str, Enum):
    """Energy levels for activities."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SocialLevel(str, Enum):
    """Social preference levels."""
    SOLO = "solo"
    SMALL_GROUP = "small_group"
    LARGE_GROUP = "large_group"


class ActivityLocation(str, Enum):
    """Location preferences for activities."""
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    EITHER = "either"


class SkillLevel(str, Enum):
    """Skill levels for activities."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MealType(str, Enum):
    """Types of meals."""
    SNACK = "snack"
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    DESSERT = "dessert"


class TimeUnit(str, Enum):
    """Time units."""
    MINUTES = "minutes"
    HOURS = "hours"


class Location(BaseModel):
    """Location data model."""
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    allow_location_access: bool = Field(default=True, description="Whether user allows location access")


class FoodPreferences(BaseModel):
    """Food and cooking preferences."""
    want_to_cook: bool = Field(default=False, description="Whether user wants to cook")
    dietary_restrictions: List[str] = Field(default=[], description="Dietary restrictions")
    skill_level: SkillLevel = Field(default=SkillLevel.BEGINNER, description="Cooking skill level")
    meal_type: MealType = Field(default=MealType.LUNCH, description="Type of meal")
    kitchen_equipment: List[str] = Field(default=[], description="Available kitchen equipment")


class ActivityPreferences(BaseModel):
    """Activity preferences."""
    location: ActivityLocation = Field(default=ActivityLocation.EITHER, description="Indoor/outdoor preference")
    social_level: SocialLevel = Field(default=SocialLevel.SOLO, description="Social preference")
    activity_types: List[ActivityType] = Field(default=[], description="Preferred activity types")
    energy_level: EnergyLevel = Field(default=EnergyLevel.MEDIUM, description="Energy level")
    mood: str = Field(default="", description="Current mood or goal")
    custom_categories: List[str] = Field(default=[], description="Custom activity categories entered by user")


class SuggestionRequest(BaseModel):
    """Request model for activity suggestions."""
    budget: float = Field(..., ge=0, description="Available budget")
    currency: str = Field(default="USD", description="Currency code")
    time_available: int = Field(..., gt=0, description="Available time")
    time_unit: TimeUnit = Field(default=TimeUnit.MINUTES, description="Time unit")
    location: Optional[Location] = Field(None, description="User location")
    food_preferences: Optional[FoodPreferences] = Field(None, description="Food preferences")
    activity_preferences: ActivityPreferences = Field(..., description="Activity preferences")


class ActivitySuggestion(BaseModel):
    """Activity suggestion model."""
    type: str = Field(..., description="Type of suggestion (ai_generated, local_business, etc.)")
    title: str = Field(..., description="Activity title")
    description: str = Field(..., description="Activity description")
    time_required: int = Field(..., description="Time required in minutes")
    cost: float = Field(..., ge=0, description="Estimated cost")
    difficulty: str = Field(..., description="Difficulty level")
    distance: Optional[str] = Field(None, description="Distance from user")
    address: Optional[str] = Field(None, description="Activity address")
    weather_appropriate: Optional[bool] = Field(None, description="Whether activity is weather appropriate")
    ai_reasoning: Optional[str] = Field(None, description="AI reasoning for suggestion")
    instructions: List[str] = Field(default=[], description="Step-by-step instructions")
    materials_needed: List[str] = Field(default=[], description="Required materials")
    hours: Optional[str] = Field(None, description="Business hours")
    rating: Optional[float] = Field(None, description="Rating if applicable")


class WeatherInfo(BaseModel):
    """Weather information model."""
    current: str = Field(..., description="Current weather description")
    suitable_for_outdoor: bool = Field(..., description="Whether weather is suitable for outdoor activities")
    temperature: Optional[float] = Field(None, description="Temperature")
    humidity: Optional[float] = Field(None, description="Humidity percentage")


class AIMetadata(BaseModel):
    """AI processing metadata."""
    model_used: str = Field(..., description="AI model used for suggestions")
    reasoning: str = Field(..., description="AI reasoning process")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")


class SuggestionResponse(BaseModel):
    """Response model for activity suggestions."""
    suggestions: List[ActivitySuggestion] = Field(..., description="List of activity suggestions")
    weather: Optional[WeatherInfo] = Field(None, description="Weather information")
    ai_metadata: Optional[AIMetadata] = Field(None, description="AI processing metadata")
    total_suggestions: int = Field(..., description="Total number of suggestions")
    request_id: Optional[str] = Field(None, description="Request identifier for tracking")


class ActivityCategory(BaseModel):
    """Activity category model."""
    id: str = Field(..., description="Category identifier")
    name: str = Field(..., description="Display name for category")
    description: str = Field(..., description="Category description")
    icon: Optional[str] = Field(None, description="Icon identifier for UI")
    examples: List[str] = Field(default=[], description="Example activities in this category")


class CustomActivityRequest(BaseModel):
    """Request model for custom activity category."""
    category_name: str = Field(..., min_length=1, max_length=50, description="Custom category name")
    description: Optional[str] = Field(None, max_length=200, description="Optional description")


class ActivitiesResponse(BaseModel):
    """Response model for activities endpoint."""
    predefined_categories: List[ActivityCategory] = Field(..., description="Predefined activity categories")
    activity_types: List[Dict[str, str]] = Field(..., description="Available activity types with descriptions")
    energy_levels: List[Dict[str, str]] = Field(..., description="Available energy levels")
    social_levels: List[Dict[str, str]] = Field(..., description="Available social preferences")
    skill_levels: List[Dict[str, str]] = Field(..., description="Available skill levels")
    supports_custom_categories: bool = Field(default=True, description="Whether custom categories are supported")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: Optional[str] = Field(None, description="Error timestamp")
