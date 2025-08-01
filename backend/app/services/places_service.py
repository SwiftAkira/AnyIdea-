"""
Google Places API service for location-based venue recommendations.
"""
import logging
import httpx
from typing import List, Dict, Any, Optional
from config import settings

logger = logging.getLogger(__name__)


class PlacesService:
    """Service for Google Places API integration."""
    
    def __init__(self):
        self.api_key = settings.google_places_api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    def is_available(self) -> bool:
        """Check if Google Places API is available."""
        return bool(self.api_key)
    
    async def search_nearby_places(
        self,
        latitude: float,
        longitude: float,
        place_type: str = "point_of_interest",
        radius: int = 5000,
        keyword: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for nearby places using Google Places API.
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            place_type: Type of place to search for
            radius: Search radius in meters (max 50000)
            keyword: Optional keyword to filter results
            max_results: Maximum number of results to return
            
        Returns:
            List of nearby places with details
        """
        if not self.is_available():
            logger.warning("Google Places API key not configured")
            return []
            
        try:
            # Use Nearby Search API
            url = f"{self.base_url}/nearbysearch/json"
            
            params = {
                "location": f"{latitude},{longitude}",
                "radius": min(radius, 50000),  # Max radius is 50km
                "type": place_type,
                "key": self.api_key
            }
            
            if keyword:
                params["keyword"] = keyword
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("status") != "OK":
                    logger.error(f"Google Places API error: {data.get('status')}")
                    return []
                
                places = []
                results = data.get("results", [])[:max_results]
                
                for place in results:
                    place_info = {
                        "name": place.get("name", "Unknown Place"),
                        "place_id": place.get("place_id"),
                        "rating": place.get("rating"),
                        "user_ratings_total": place.get("user_ratings_total"),
                        "price_level": place.get("price_level"),
                        "types": place.get("types", []),
                        "vicinity": place.get("vicinity"),
                        "geometry": place.get("geometry", {}),
                        "photos": place.get("photos", []),
                        "opening_hours": place.get("opening_hours", {}),
                        "permanently_closed": place.get("permanently_closed", False)
                    }
                    places.append(place_info)
                
                logger.info(f"Found {len(places)} nearby places for type '{place_type}'")
                return places
                
        except Exception as e:
            logger.error(f"Error searching nearby places: {e}")
            return []
    
    async def get_activity_venues(
        self,
        latitude: float,
        longitude: float,
        activity_type: str,
        budget_level: str = "moderate",
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """
        Get venue recommendations based on activity type and budget.
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            activity_type: Type of activity (e.g., 'restaurant', 'gym', 'museum')
            budget_level: Budget level (free, low, moderate, high)
            radius: Search radius in meters
            
        Returns:
            List of recommended venues
        """
        # Map activity types to Google Places types and keywords
        activity_mapping = {
            "food": {
                "type": "restaurant",
                "keywords": ["restaurant", "cafe", "food"]
            },
            "entertainment": {
                "type": "movie_theater",
                "keywords": ["cinema", "theater", "entertainment"]
            },
            "exercise": {
                "type": "gym",
                "keywords": ["gym", "fitness", "sports", "park"]
            },
            "shopping": {
                "type": "shopping_mall",
                "keywords": ["shopping", "store", "mall"]
            },
            "culture": {
                "type": "museum",
                "keywords": ["museum", "gallery", "cultural", "art"]
            },
            "outdoor": {
                "type": "park",
                "keywords": ["park", "outdoor", "nature", "hiking"]
            },
            "learning": {
                "type": "library",
                "keywords": ["library", "bookstore", "education", "learning"]
            }
        }
        
        mapping = activity_mapping.get(activity_type, {
            "type": "point_of_interest",
            "keywords": [activity_type]
        })
        
        venues = []
        
        # Search with primary type
        primary_venues = await self.search_nearby_places(
            latitude=latitude,
            longitude=longitude,
            place_type=mapping["type"],
            radius=radius,
            max_results=5
        )
        venues.extend(primary_venues)
        
        # Search with keywords for more variety
        for keyword in mapping["keywords"][:2]:  # Limit to 2 keywords to avoid rate limits
            keyword_venues = await self.search_nearby_places(
                latitude=latitude,
                longitude=longitude,
                place_type="establishment",
                keyword=keyword,
                radius=radius,
                max_results=3
            )
            venues.extend(keyword_venues)
        
        # Remove duplicates based on place_id
        unique_venues = {}
        for venue in venues:
            place_id = venue.get("place_id")
            if place_id and place_id not in unique_venues:
                unique_venues[place_id] = venue
        
        # Filter by budget if price_level is available
        filtered_venues = list(unique_venues.values())
        if budget_level != "any":
            budget_mapping = {
                "free": [0],
                "low": [0, 1],
                "moderate": [0, 1, 2],
                "high": [0, 1, 2, 3, 4]
            }
            allowed_prices = budget_mapping.get(budget_level, [0, 1, 2, 3, 4])
            
            filtered_venues = [
                venue for venue in filtered_venues
                if venue.get("price_level") is None or venue.get("price_level") in allowed_prices
            ]
        
        # Sort by rating and user reviews
        filtered_venues.sort(
            key=lambda x: (
                x.get("rating", 0) * (1 + min(x.get("user_ratings_total", 0) / 100, 1)),
                -x.get("permanently_closed", False)
            ),
            reverse=True
        )
        
        logger.info(f"Found {len(filtered_venues)} venues for activity '{activity_type}' with budget '{budget_level}'")
        return filtered_venues[:8]  # Return top 8 venues


# Global service instance
places_service = PlacesService()
