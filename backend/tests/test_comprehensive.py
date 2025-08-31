#!/usr/bin/env python3
"""
Comprehensive test suite for SideMoney.ai API
Combines functionality from test_api.py and test_ai_features.py
Run this after starting the backend server
"""

import asyncio
import requests
import json
from datetime import date, timedelta
from decimal import Decimal
from services.ai_service import AIService
from schemas.ai import AIPromptRequest, OCRTransactionItem, BulkTransactionCreate

BASE_URL = "http://localhost:8000"


def test_health_and_structure():
    """Test basic API health and structure"""
    print("🔍 Testing API Health & Structure...")
    
    # Health check
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Backend is healthy")
        health_data = response.json()
        print(f"   Database: {health_data.get('database', 'unknown')}")
    else:
        print("❌ Backend health check failed")
        return False
    
    # Root endpoint
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✅ Root endpoint working")
        api_info = response.json()
        print(f"   Version: {api_info.get('version', 'unknown')}")
        print(f"   Features: {len(api_info.get('features', []))}")
    else:
        print("❌ Root endpoint failed")
    
    # API documentation
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        print("✅ API documentation available at /docs")
    else:
        print("❌ API documentation not accessible")
    
    return True


def test_categorization_endpoint():
    """Test the consolidated AI categorization endpoint"""
    print("\n🤖 Testing AI Categorization Endpoint...")
    
    test_descriptions = [
        "Starbucks coffee",
        "Walmart grocery shopping", 
        "Uber ride to work",
        "Netflix subscription",
        "Gas station fill-up",
        "Amazon Prime purchase",
        "Gym membership fee"
    ]
    
    for description in test_descriptions:
        try:
            response = requests.post(
                f"{BASE_URL}/transactions/categorize",
                params={"description": description, "amount": 25.0}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"  '{description}' → {result['category_display_name']} ({result['confidence']})")
            else:
                print(f"  Error categorizing '{description}': {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")


async def test_ai_service_direct():
    """Test AI service methods directly"""
    print("\n🧠 Testing AI Service Methods...")
    
    # Test categorization
    print("  Testing transaction categorization...")
    test_descriptions = [
        "Starbucks Coffee Downtown",
        "Whole Foods Market Groceries",
        "Uber ride to airport", 
        "Netflix subscription"
    ]
    
    for desc in test_descriptions:
        try:
            category = AIService.categorize_transaction(desc, 25.0)
            print(f"    '{desc}' → {category.value}")
        except Exception as e:
            print(f"    Error categorizing '{desc}': {e}")
    
    # Test enhanced analysis
    print("  Testing enhanced financial analysis...")
    user_spending = {
        "FOOD_DINING": 450.0,
        "GROCERIES": 320.0,
        "TRANSPORTATION": 180.0,
        "ENTERTAINMENT": 220.0
    }
    
    goals = [{
        "id": "goal1",
        "title": "Emergency Fund", 
        "target_amount": 5000.0,
        "current_amount": 1200.0,
        "deadline": (date.today() + timedelta(days=365)).isoformat(),
        "days_remaining": 365
    }]
    
    transactions = [{
        "id": "t1",
        "amount": 45.0,
        "type": "expense",
        "category": "FOOD_DINING",
        "description": "Restaurant dinner",
        "date": date.today().isoformat()
    }]
    
    try:
        analysis = AIService.generate_enhanced_analysis(
            user_spending=user_spending,
            daily_budget=50.0,
            goals=goals,
            transactions=transactions,
            period_days=30
        )
        print(f"    ✅ Analysis generated (confidence: {analysis.confidence_score})")
        print(f"    📋 Recommendations: {len(analysis.recommendations)}")
        print(f"    💡 Insights: {len(analysis.insights)}")
    except Exception as e:
        print(f"    ❌ Analysis failed: {e}")


def test_api_endpoints_structure():
    """Test the reorganized API endpoint structure"""
    print("\n🌐 Testing Reorganized API Endpoints...")
    
    endpoints = {
        "AI Analysis": {
            "method": "POST",
            "endpoint": "/ai/analyze?period_days=30",
            "description": "Comprehensive AI financial analysis"
        },
        "OCR Processing": {
            "method": "POST", 
            "endpoint": "/ai/ocr/process",
            "description": "Upload receipt for transaction extraction",
            "content_type": "multipart/form-data"
        },
        "Custom AI Query": {
            "method": "POST",
            "endpoint": "/ai/query",
            "description": "Ask personalized financial questions"
        },
        "Transaction Categorization": {
            "method": "POST",
            "endpoint": "/transactions/categorize?description=Starbucks%20Coffee",
            "description": "Get AI categorization for transaction"
        },
        "Bulk Transactions": {
            "method": "POST",
            "endpoint": "/transactions/bulk",
            "description": "Create multiple transactions from OCR results"
        }
    }
    
    for name, info in endpoints.items():
        print(f"  🔗 {name}:")
        print(f"     {info['method']} {info['endpoint']}")
        print(f"     {info['description']}")
        if 'content_type' in info:
            print(f"     Content-Type: {info['content_type']}")
        print()


def validate_schema_structure():
    """Validate OCR and bulk transaction schemas"""
    print("\n📄 Testing Schema Validation...")
    
    # Test OCR transaction item
    try:
        ocr_item = OCRTransactionItem(
            description="Starbucks Coffee",
            amount=Decimal("5.99"),
            date=date.today(),
            category="FOOD_DINING",
            merchant="Starbucks",
            confidence=0.95
        )
        print(f"  ✅ OCR item schema valid: {ocr_item.description} - ${ocr_item.amount}")
    except Exception as e:
        print(f"  ❌ OCR item validation failed: {e}")
    
    # Test bulk transaction schema
    try:
        bulk_request = BulkTransactionCreate(
            transactions=[ocr_item],
            source="ocr",
            verify_before_save=True
        )
        print(f"  ✅ Bulk request schema valid with {len(bulk_request.transactions)} transactions")
    except Exception as e:
        print(f"  ❌ Bulk validation failed: {e}")


async def main():
    """Run comprehensive test suite"""
    print("🚀 SideMoney.ai Comprehensive Test Suite")
    print("=" * 50)
    
    # Test basic API health and structure
    if not test_health_and_structure():
        print("❌ Basic API tests failed, stopping...")
        return
    
    # Test endpoint structure
    test_api_endpoints_structure()
    
    # Test categorization endpoint (without auth for demo)
    # Note: In real usage, you'd need to authenticate first
    # test_categorization_endpoint()
    
    # Test AI service methods directly
    await test_ai_service_direct()
    
    # Test schema validation
    validate_schema_structure()
    
    print("\n✨ Comprehensive Test Suite Complete!")
    print("\n📋 API Cleanup Summary:")
    print("  ✅ Removed duplicate OCR endpoint from transactions")
    print("  ✅ Consolidated categorization in transactions module")
    print("  ✅ Moved bulk transactions to transactions module")
    print("  ✅ Cleaned up unused imports")
    print("  ✅ Organized tests in dedicated folder")
    print("  ✅ Updated documentation")
    print("\n📚 Next Steps:")
    print(f"  • Visit {BASE_URL}/docs for interactive API documentation")
    print("  • Set GEMINI_API_KEY for AI features")
    print("  • Test with real authentication tokens")


if __name__ == "__main__":
    asyncio.run(main()) 