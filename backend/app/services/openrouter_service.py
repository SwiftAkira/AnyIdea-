"""
OpenRouter AI service for generating intelligent activity suggestions.
"""
import httpx
import logging
from typing import List, Dict, Any, Optional
from config import settings

logger = logging.getLogger(__name__)


class OpenRouterService:
    """Service for interacting with OpenRouter AI API."""
    
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AnyIdea? Activity Suggestions",
            "Content-Type": "application/json"
        }
    
    async def get_activity_suggestions(
        self,
        budget: float,
        time_available: int,
        location_data: Optional[Dict[str, Any]] = None,
        weather_data: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None,
        custom_categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI-powered activity suggestions using OpenRouter.
        
        Args:
            budget: Available budget
            time_available: Available time in minutes
            location_data: User location information
            weather_data: Current weather data
            preferences: User preferences
            custom_categories: Custom activity categories provided by user
            
        Returns:
            Dictionary containing AI suggestions and metadata
        """
        try:
            # Construct the prompt
            prompt = self._build_prompt(
                budget=budget,
                time_available=time_available,
                location_data=location_data,
                weather_data=weather_data,
                preferences=preferences,
                custom_categories=custom_categories
            )
            
            # Prepare the API request
            payload = {
                "model": "moonshotai/kimi-k2:free",  # Using Kimi-K2 free model
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return self._parse_ai_response(result)
                else:
                    logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                    return self._get_fallback_response()
                    
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {e}")
            return self._get_fallback_response()
    
    def _build_prompt(
        self,
        budget: float,
        time_available: int,
        location_data: Optional[Dict[str, Any]] = None,
        weather_data: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None,
        custom_categories: Optional[List[str]] = None
    ) -> str:
        """Build a structured prompt for the AI."""
        
        prompt_parts = [
            f"I have ${budget} budget and {time_available} minutes available.",
            "I need 2-3 specific, actionable activity suggestions."
        ]
        
        if preferences:
            if preferences.get("location"):
                prompt_parts.append(f"I prefer {preferences['location']} activities.")
            if preferences.get("energy_level"):
                prompt_parts.append(f"My energy level is {preferences['energy_level']}.")
            if preferences.get("activity_types"):
                types = ", ".join(preferences["activity_types"])
                prompt_parts.append(f"I'm interested in: {types}.")
            if preferences.get("mood"):
                prompt_parts.append(f"My current mood/goal: {preferences['mood']}.")
        
        # Handle custom categories
        if custom_categories:
            custom_types = ", ".join(custom_categories)
            prompt_parts.append(f"I'm also interested in these custom activity types: {custom_types}.")
            prompt_parts.append("Please consider these custom categories when making suggestions.")
        
        if weather_data:
            prompt_parts.append(f"Current weather: {weather_data.get('current', 'unknown')}.")
        
        if location_data and location_data.get("allow_location_access"):
            prompt_parts.append("I'm open to location-based suggestions.")
        
        prompt_parts.extend([
            "",
            "Please respond with ONLY a JSON object in this exact format:",
            "{",
            '  "suggestions": [',
            '    {',
            '      "title": "Activity Title",',
            '      "description": "Brief description",',
            '      "time_required": 30,',
            '      "cost": 5.0,',
            '      "difficulty": "easy",',
            '      "instructions": ["Step 1", "Step 2", "Step 3"],',
            '      "materials_needed": ["item1", "item2"]',
            '    }',
            '  ],',
            '  "reasoning": "Why these suggestions fit the user\'s needs"',
            "}"
        ])
        
        return "\n".join(prompt_parts)
    
    def _parse_ai_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the OpenRouter API response."""
        try:
            content = response["choices"][0]["message"]["content"]
            logger.debug(f"AI response content: {content[:500]}...")  # Log first 500 chars for debugging
            
            # Try to extract JSON from the response
            import json
            
            # Find JSON content (sometimes AI adds extra text)
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                logger.debug(f"Extracted JSON string: {json_str[:200]}...")  # Log JSON for debugging
                ai_data = json.loads(json_str)
                
                return {
                    "suggestions": ai_data.get("suggestions", []),
                    "model_used": response.get("model", "moonshotai/kimi-k2:free"),
                    "reasoning": ai_data.get("reasoning", "AI-generated suggestions"),
                    "processing_time": 0.5,  # Approximate
                    "success": True
                }
            else:
                logger.warning(f"Could not extract JSON from AI response. Content: {content[:200]}...")
                return self._get_fallback_response()
                
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Return fallback response when AI fails."""
        return {
            "suggestions": [
                {
                    "title": "Take a mindful break",
                    "description": "Step away from screens and take a few deep breaths",
                    "time_required": 10,
                    "cost": 0.0,
                    "difficulty": "easy",
                    "instructions": [
                        "Find a quiet spot",
                        "Sit comfortably",
                        "Take 10 deep breaths",
                        "Focus on the present moment"
                    ],
                    "materials_needed": []
                }
            ],
            "model_used": "fallback",
            "reasoning": "AI service unavailable, providing fallback suggestion",
            "processing_time": 0.0,
            "success": False
        }
    
    def is_available(self) -> bool:
        """Check if OpenRouter service is available."""
        return bool(self.api_key and self.api_key.strip())


# Global service instance
openrouter_service = OpenRouterService()
