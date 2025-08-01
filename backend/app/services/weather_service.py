"""
Weather service for getting current weather conditions.
Using WeatherAPI.com for weather data.
"""
import httpx
import logging
from typing import Dict, Any, Optional
from config import settings

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for getting weather information."""
    
    def __init__(self):
        self.api_key = settings.weather_api_key
        self.base_url = "http://api.weatherapi.com/v1"
    
    async def get_current_weather(
        self, 
        latitude: float, 
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Get current weather for the given coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Weather data dictionary or None if failed
        """
        if not self.is_available():
            logger.warning("Weather API key not configured")
            return self._get_fallback_weather()
        
        try:
            # WeatherAPI uses lat,lon format
            location = f"{latitude},{longitude}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/current.json",
                    params={
                        "key": self.api_key,
                        "q": location,
                        "aqi": "no"  # We don't need air quality data
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_weather_response(data)
                else:
                    logger.error(f"Weather API error: {response.status_code} - {response.text}")
                    return self._get_fallback_weather()
                    
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return self._get_fallback_weather()
    
    async def get_weather_by_city(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Get current weather for a city name.
        
        Args:
            city: City name
            
        Returns:
            Weather data dictionary or None if failed
        """
        if not self.is_available():
            return self._get_fallback_weather()
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/current.json",
                    params={
                        "key": self.api_key,
                        "q": city,
                        "aqi": "no"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_weather_response(data)
                else:
                    logger.error(f"Weather API error: {response.status_code} - {response.text}")
                    return self._get_fallback_weather()
                    
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return self._get_fallback_weather()
    
    def _parse_weather_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the WeatherAPI response into our format."""
        try:
            current = data["current"]
            location = data["location"]
            
            # Temperature in Fahrenheit
            temp_f = current["temp_f"]
            temp_c = current["temp_c"]
            condition = current["condition"]["text"]
            humidity = current["humidity"]
            wind_mph = current["wind_mph"]
            
            # Determine if suitable for outdoor activities
            # Consider temperature, precipitation, and wind
            is_raining = "rain" in condition.lower() or "drizzle" in condition.lower()
            is_snowing = "snow" in condition.lower()
            is_stormy = "storm" in condition.lower() or "thunder" in condition.lower()
            is_very_windy = wind_mph > 25
            is_extreme_temp = temp_f < 32 or temp_f > 95
            
            suitable_for_outdoor = not (is_raining or is_snowing or is_stormy or is_very_windy or is_extreme_temp)
            
            return {
                "current": f"{condition}, {int(temp_f)}°F",
                "suitable_for_outdoor": suitable_for_outdoor,
                "temperature": temp_f,
                "temperature_c": temp_c,
                "humidity": humidity,
                "condition": condition,
                "wind_mph": wind_mph,
                "location": f"{location['name']}, {location['region']}",
                "local_time": location["localtime"]
            }
            
        except KeyError as e:
            logger.error(f"Error parsing weather response: missing key {e}")
            return self._get_fallback_weather()
    
    def _get_fallback_weather(self) -> Dict[str, Any]:
        """Return fallback weather data when API is unavailable."""
        return {
            "current": "Weather unavailable",
            "suitable_for_outdoor": True,  # Default to optimistic
            "temperature": 70.0,
            "humidity": 50.0,
            "condition": "Unknown",
            "wind_mph": 5.0,
            "location": "Unknown location",
            "local_time": "Unknown"
        }
    
    def is_available(self) -> bool:
        """Check if Weather service is available."""
        return bool(self.api_key and self.api_key.strip())


# Global service instance
weather_service = WeatherService()
