#!/usr/bin/env python3
"""
Simple test script to demonstrate the SideMoney.ai API
Run this after starting the backend server
"""

import requests
import json
from datetime import date, timedelta
from decimal import Decimal

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_categorization():
    """Test the AI categorization endpoint"""
    print("\n🤖 Testing AI categorization...")
    
    test_descriptions = [
        "Starbucks coffee",
        "Walmart grocery shopping",
        "Uber ride to work",
        "Netflix subscription",
        "Gas station fill-up"
    ]
    
    for description in test_descriptions:
        try:
            response = requests.post(
                f"{BASE_URL}/transactions/categorize",
                params={"description": description}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"'{description}' → {result['category_display_name']}")
            else:
                print(f"Error categorizing '{description}': {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")


def test_api_structure():
    """Test the API structure and endpoints"""
    print("\n📊 Testing API structure...")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✅ Root endpoint working")
        print(f"API Info: {response.json()}")
    else:
        print("❌ Root endpoint failed")
    
    # Test OpenAPI docs
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        print("✅ API documentation available at /docs")
    else:
        print("❌ API documentation not accessible")


if __name__ == "__main__":
    print("🚀 SideMoney.ai Backend API Test")
    print("=" * 50)
    
    # Test health check
    if test_health_check():
        print("✅ Backend is healthy")
    else:
        print("❌ Backend health check failed")
        exit(1)
    
    # Test API structure
    test_api_structure()
    
    # Test categorization (without auth for demo)
    # Note: In real usage, you'd need to authenticate first
    # test_categorization()
    
    print("\n🎉 API test complete!")
    print(f"📚 Visit {BASE_URL}/docs for interactive API documentation") 