"""
Test file demonstrating AI features and Gemini integration
Run with: python test_ai_features.py
"""

import asyncio
import json
from datetime import date, timedelta
from decimal import Decimal
from services.ai_service import AIService
from schemas.ai import AIPromptRequest, OCRTransactionItem, BulkTransactionCreate


async def test_transaction_categorization():
    """Test AI-powered transaction categorization"""
    print("\n🔍 Testing Transaction Categorization...")
    
    test_descriptions = [
        "Starbucks Coffee Downtown",
        "Whole Foods Market Groceries", 
        "Uber ride to airport",
        "Netflix subscription",
        "Shell Gas Station",
        "Amazon Prime purchase",
        "Gym membership fee",
        "Doctor appointment copay"
    ]
    
    for desc in test_descriptions:
        category = AIService.categorize_transaction(desc, 25.0)
        print(f"  '{desc}' → {category.value}")


async def test_enhanced_analysis():
    """Test enhanced financial analysis with Gemini"""
    print("\n📊 Testing Enhanced Financial Analysis...")
    
    # Sample user data
    user_spending = {
        "FOOD_DINING": 450.0,
        "GROCERIES": 320.0,
        "TRANSPORTATION": 180.0,
        "ENTERTAINMENT": 220.0,
        "SHOPPING": 380.0
    }
    
    daily_budget = 50.0
    
    goals = [
        {
            "id": "goal1",
            "title": "Emergency Fund",
            "target_amount": 5000.0,
            "current_amount": 1200.0,
            "deadline": (date.today() + timedelta(days=365)).isoformat(),
            "days_remaining": 365
        },
        {
            "id": "goal2", 
            "title": "Vacation Fund",
            "target_amount": 2000.0,
            "current_amount": 800.0,
            "deadline": (date.today() + timedelta(days=120)).isoformat(),
            "days_remaining": 120
        }
    ]
    
    transactions = [
        {
            "id": "t1",
            "amount": 45.0,
            "type": "expense",
            "category": "FOOD_DINING",
            "description": "Restaurant dinner",
            "date": date.today().isoformat()
        },
        {
            "id": "t2",
            "amount": 85.0,
            "type": "expense", 
            "category": "GROCERIES",
            "description": "Weekly groceries",
            "date": (date.today() - timedelta(days=1)).isoformat()
        }
    ]
    
    try:
        analysis = AIService.generate_enhanced_analysis(
            user_spending=user_spending,
            daily_budget=daily_budget,
            goals=goals,
            transactions=transactions,
            period_days=30
        )
        
        print(f"  ✅ Analysis generated with confidence: {analysis.confidence_score}")
        print(f"  📋 Recommendations: {len(analysis.recommendations)}")
        print(f"  💡 Insights: {len(analysis.insights)}")
        print(f"  📝 Summary: {analysis.summary[:100]}...")
        
        # Display first recommendation
        if analysis.recommendations:
            rec = analysis.recommendations[0]
            print(f"  🎯 Top Recommendation: {rec.title}")
            print(f"     Priority: {rec.priority.value}")
            print(f"     Potential Savings: ${rec.potential_savings}")
            
    except Exception as e:
        print(f"  ❌ Analysis failed: {e}")


async def test_custom_ai_query():
    """Test custom AI query functionality"""
    print("\n❓ Testing Custom AI Query...")
    
    request = AIPromptRequest(
        user_query="How can I save more money for my vacation goal?",
        include_transactions=True,
        include_goals=True,
        include_budget=True,
        period_days=30
    )
    
    user_data = {
        "daily_budget": 50.0,
        "transactions": [
            {
                "amount": 45.0,
                "type": "expense",
                "category": "FOOD_DINING",
                "description": "Restaurant dinner",
                "date": date.today().isoformat()
            }
        ],
        "goals": [
            {
                "title": "Vacation Fund",
                "target_amount": 2000.0,
                "current_amount": 800.0,
                "deadline": (date.today() + timedelta(days=120)).isoformat(),
                "days_remaining": 120
            }
        ]
    }
    
    try:
        response = await AIService.custom_ai_query(request, user_data)
        print(f"  ✅ Query processed with confidence: {response.confidence}")
        print(f"  📝 Response: {response.response[:150]}...")
        print(f"  💡 Suggestions: {len(response.suggestions)}")
        
    except Exception as e:
        print(f"  ❌ Query failed: {e}")


def test_ocr_schema_validation():
    """Test OCR transaction schema validation"""
    print("\n📄 Testing OCR Schema Validation...")
    
    # Test valid OCR transaction
    try:
        ocr_item = OCRTransactionItem(
            description="Starbucks Coffee",
            amount=Decimal("5.99"),
            date=date.today(),
            category="FOOD_DINING",
            merchant="Starbucks",
            confidence=0.95
        )
        print(f"  ✅ Valid OCR item: {ocr_item.description} - ${ocr_item.amount}")
        
    except Exception as e:
        print(f"  ❌ OCR validation failed: {e}")
    
    # Test bulk transaction creation schema
    try:
        bulk_request = BulkTransactionCreate(
            transactions=[ocr_item],
            source="ocr",
            verify_before_save=True
        )
        print(f"  ✅ Bulk request valid with {len(bulk_request.transactions)} transactions")
        
    except Exception as e:
        print(f"  ❌ Bulk validation failed: {e}")


def test_prompt_engineering():
    """Test prompt engineering structure"""
    print("\n🎯 Testing Prompt Engineering...")
    
    # Test financial analysis prompt
    user_spending = {"FOOD_DINING": 200.0, "GROCERIES": 150.0}
    daily_budget = 40.0
    goals = []
    transactions = []
    
    prompt = AIService._create_financial_analysis_prompt(
        user_spending, daily_budget, goals, transactions, 30
    )
    
    print(f"  ✅ Financial analysis prompt generated ({len(prompt)} characters)")
    print(f"  📋 Contains structured output format: {'OUTPUT FORMAT (JSON)' in prompt}")
    print(f"  🎯 Contains user data: {'SPENDING BY CATEGORY' in prompt}")
    
    # Test OCR prompt
    ocr_prompt = AIService._create_ocr_prompt()
    print(f"  ✅ OCR prompt generated ({len(ocr_prompt)} characters)")
    print(f"  🔍 Contains extraction rules: {'EXTRACTION RULES' in ocr_prompt}")
    print(f"  📊 Contains output format: {'OUTPUT FORMAT (JSON)' in ocr_prompt}")


def print_api_examples():
    """Print example API usage"""
    print("\n🌐 API Usage Examples:")
    
    examples = {
        "Enhanced Analysis": {
            "method": "POST",
            "endpoint": "/ai/analyze?period_days=30",
            "description": "Get comprehensive AI financial analysis"
        },
        "OCR Processing": {
            "method": "POST", 
            "endpoint": "/ai/ocr/process",
            "description": "Upload receipt image for transaction extraction",
            "content_type": "multipart/form-data"
        },
        "Bulk Transactions": {
            "method": "POST",
            "endpoint": "/transactions/bulk", 
            "description": "Create multiple transactions from OCR results"
        },
        "Custom AI Query": {
            "method": "POST",
            "endpoint": "/ai/query",
            "description": "Ask personalized financial questions"
        },
        "AI Categorization": {
            "method": "POST",
            "endpoint": "/transactions/categorize?description=Starbucks%20Coffee",
            "description": "Get AI categorization for transaction"
        }
    }
    
    for name, info in examples.items():
        print(f"  🔗 {name}:")
        print(f"     {info['method']} {info['endpoint']}")
        print(f"     {info['description']}")
        if 'content_type' in info:
            print(f"     Content-Type: {info['content_type']}")
        print()


async def main():
    """Run all AI feature tests"""
    print("🤖 SideMoney.ai AI Features Test Suite")
    print("=" * 50)
    
    # Test categorization
    await test_transaction_categorization()
    
    # Test enhanced analysis
    await test_enhanced_analysis()
    
    # Test custom queries
    await test_custom_ai_query()
    
    # Test schema validation
    test_ocr_schema_validation()
    
    # Test prompt engineering
    test_prompt_engineering()
    
    # Print API examples
    print_api_examples()
    
    print("\n✨ AI Features Test Complete!")
    print("\n📋 Setup Checklist:")
    print("  □ Set GEMINI_API_KEY in environment")
    print("  □ Install google-generativeai package")
    print("  □ Test with real receipt images")
    print("  □ Configure rate limiting for production")
    print("  □ Set up monitoring for AI API usage")


if __name__ == "__main__":
    asyncio.run(main()) 