#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced activities API functionality.
"""
import asyncio
import httpx
import json
from typing import Dict, Any
import pytest


@pytest.mark.asyncio
async def test_activities_endpoints():
    """Test all the new activities-related endpoints."""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing AnyIdea? Activities API")
        print("=" * 50)
        
        # Test 1: Get predefined categories
        print("\n1️⃣ Testing GET /api/activities")
        response = await client.get(f"{base_url}/api/activities")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data['predefined_categories'])} predefined categories")
            print("📋 Available categories:")
            for cat in data['predefined_categories'][:3]:  # Show first 3
                print(f"   • {cat['name']}: {cat['description']}")
            print(f"   ... and {len(data['predefined_categories']) - 3} more")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        # Test 2: Create a valid custom category
        print("\n2️⃣ Testing POST /api/activities/custom (valid)")
        custom_request = {
            "category_name": "Eco-Friendly Projects",
            "description": "Sustainable and environmentally conscious activities"
        }
        response = await client.post(
            f"{base_url}/api/activities/custom",
            json=custom_request
        )
        if response.status_code == 200:
            data = response.json()
            if data["accepted"]:
                print(f"✅ Custom category '{data['category']['name']}' accepted!")
                print(f"   ID: {data['category']['id']}")
            else:
                print(f"⚠️  Category rejected: {data['message']}")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        # Test 3: Try to create a duplicate category
        print("\n3️⃣ Testing POST /api/activities/custom (duplicate)")
        duplicate_request = {
            "category_name": "Creative"
        }
        response = await client.post(
            f"{base_url}/api/activities/custom",
            json=duplicate_request
        )
        if response.status_code == 200:
            data = response.json()
            if not data["accepted"]:
                print(f"✅ Correctly rejected duplicate: {data['message']}")
            else:
                print("❌ Should have rejected duplicate category")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        # Test 4: Use custom category in main suggestion
        print("\n4️⃣ Testing POST /api/suggest with custom categories")
        suggestion_request = {
            "budget": 30.0,
            "time_available": 45,
            "activity_preferences": {
                "location": "indoor",
                "energy_level": "medium",
                "activity_types": ["creative", "productive"],
                "custom_categories": ["Eco-Friendly Projects"],
                "mood": "want to do something good for the environment"
            }
        }
        response = await client.post(
            f"{base_url}/api/suggest",
            json=suggestion_request
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generated {len(data['suggestions'])} suggestions with custom categories!")
            if data['suggestions']:
                first_suggestion = data['suggestions'][0]
                print(f"   🎯 First suggestion: {first_suggestion['title']}")
                print(f"   💰 Cost: ${first_suggestion['cost']}")
                print(f"   ⏱️  Time: {first_suggestion['time_required']} minutes")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        print("\n🎉 All tests completed!")
        print("\n📖 Summary of new features:")
        print("   • Rich predefined activity categories with descriptions and examples")
        print("   • Custom category creation with validation")
        print("   • Duplicate detection for custom categories")
        print("   • Integration of custom categories in AI suggestions")
        print("   • Comprehensive API documentation at /docs")


if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the server is running on http://localhost:8000")
    asyncio.run(test_activities_endpoints())
