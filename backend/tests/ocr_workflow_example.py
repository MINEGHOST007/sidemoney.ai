"""
Complete OCR Workflow Example
Demonstrates receipt processing → transaction extraction → bulk creation

Usage:
1. Place a receipt image in the same directory as 'sample_receipt.jpg'
2. Run: python examples/ocr_workflow_example.py
"""

import asyncio
import json
from pathlib import Path
from datetime import date
from decimal import Decimal

# Mock classes for demonstration (replace with actual imports in real usage)
class MockAIService:
    """Mock AI service for demonstration"""
    
    @staticmethod
    async def process_receipt_ocr(image_data: bytes, filename: str):
        """Mock OCR processing - returns sample data"""
        from schemas.ai import OCRResult, OCRTransactionItem
        
        # Simulate OCR processing
        sample_transactions = [
            OCRTransactionItem(
                description="Grande Pike Place Roast",
                amount=Decimal("4.95"),
                date=date.today(),
                category="FOOD_DINING",
                merchant="Starbucks",
                confidence=0.95
            ),
            OCRTransactionItem(
                description="Blueberry Scone",
                amount=Decimal("3.25"),
                date=date.today(),
                category="FOOD_DINING", 
                merchant="Starbucks",
                confidence=0.88
            ),
            OCRTransactionItem(
                description="Sales Tax",
                amount=Decimal("0.66"),
                date=date.today(),
                category="MISCELLANEOUS",
                merchant="Starbucks",
                confidence=0.92
            )
        ]
        
        return OCRResult(
            transactions=sample_transactions,
            total_amount=sum(t.amount for t in sample_transactions),
            document_type="receipt",
            processing_confidence=0.91,
            raw_text="STARBUCKS\\n123 Main St\\n\\nGrande Pike Place Roast $4.95\\nBlueberry Scone $3.25\\nSubtotal $8.20\\nTax $0.66\\nTotal $8.86\\n\\nThank you!",
            warnings=[]
        )


async def demonstrate_ocr_workflow():
    """Demonstrate complete OCR workflow"""
    print("🤖 SideMoney.ai OCR Workflow Demonstration")
    print("=" * 50)
    
    # Step 1: Process receipt image
    print("\n📷 Step 1: Processing Receipt Image...")
    
    # In real usage, you would read an actual image file:
    # with open("sample_receipt.jpg", "rb") as f:
    #     image_data = f.read()
    
    # For demo, we'll use mock data
    image_data = b"mock_image_data"
    filename = "sample_receipt.jpg"
    
    try:
        # Process with OCR
        ocr_result = await MockAIService.process_receipt_ocr(image_data, filename)
        
        print(f"  ✅ OCR Processing Complete!")
        print(f"  📊 Document Type: {ocr_result.document_type}")
        print(f"  🎯 Processing Confidence: {ocr_result.processing_confidence:.1%}")
        print(f"  💰 Total Amount: ${ocr_result.total_amount}")
        print(f"  📝 Transactions Found: {len(ocr_result.transactions)}")
        
        if ocr_result.warnings:
            print(f"  ⚠️  Warnings: {', '.join(ocr_result.warnings)}")
        
        # Display extracted transactions
        print(f"\n  📋 Extracted Transactions:")
        for i, transaction in enumerate(ocr_result.transactions, 1):
            print(f"    {i}. {transaction.description}")
            print(f"       Amount: ${transaction.amount}")
            print(f"       Category: {transaction.category}")
            print(f"       Merchant: {transaction.merchant}")
            print(f"       Confidence: {transaction.confidence:.1%}")
            print()
        
        # Step 2: User verification (in real app, this would be a UI step)
        print("👤 Step 2: User Verification...")
        print("  In the real app, user would review and modify transactions if needed")
        print("  For demo, we'll assume user approves all transactions")
        
        # Step 3: Bulk transaction creation
        print("\n💾 Step 3: Creating Transactions in Database...")
        
        from schemas.ai import BulkTransactionCreate
        
        bulk_request = BulkTransactionCreate(
            transactions=ocr_result.transactions,
            source="ocr",
            verify_before_save=False  # Already verified by user
        )
        
        print(f"  📦 Bulk Request Created:")
        print(f"     Transactions: {len(bulk_request.transactions)}")
        print(f"     Source: {bulk_request.source}")
        print(f"     Verify Before Save: {bulk_request.verify_before_save}")
        
        # In real usage, this would call the API:
        # response = await api_client.post("/ai/transactions/bulk", json=bulk_request.dict())
        
        # Mock successful response
        print(f"  ✅ Transactions Created Successfully!")
        print(f"     Created: {len(bulk_request.transactions)} transactions")
        print(f"     Failed: 0 transactions")
        
        # Step 4: Generate insights on new data
        print("\n🧠 Step 4: Generating AI Insights...")
        
        # This would typically trigger a new analysis
        print("  🔄 Triggering financial analysis with new transaction data...")
        print("  📊 Updated spending categories and recommendations available")
        
        return True
        
    except Exception as e:
        print(f"  ❌ OCR workflow failed: {e}")
        return False


def demonstrate_prompt_engineering():
    """Show the prompt engineering structure"""
    print("\n🎯 Prompt Engineering Structure")
    print("=" * 40)
    
    # Financial Analysis Prompt Example
    print("\n📊 Financial Analysis Prompt:")
    print("```")
    sample_prompt = """
    You are a professional financial advisor AI. Analyze the user's financial data and provide structured insights.

    **USER FINANCIAL DATA:**
    - Daily Budget: $50.00
    - Period: 30 days
    - Total Budget: $1,500.00
    - Total Spending: $1,234.56
    - Total Income: $2,000.00
    
    **SPENDING BY CATEGORY:**
    {
      "FOOD_DINING": 450.0,
      "GROCERIES": 320.0,
      "TRANSPORTATION": 180.0
    }
    
    **ANALYSIS REQUIREMENTS:**
    1. Provide 3-5 personalized recommendations with specific action items
    2. Generate 3-5 data-driven insights about spending patterns
    3. Include potential savings estimates where applicable
    4. Prioritize recommendations by impact and urgency

    **OUTPUT FORMAT (JSON):**
    {
        "recommendations": [...],
        "insights": [...],
        "summary": "Overall financial health summary",
        "confidence_score": 0.85
    }
    """
    print(sample_prompt)
    print("```")
    
    # OCR Prompt Example
    print("\n📷 OCR Processing Prompt:")
    print("```")
    sample_ocr_prompt = """
    You are an expert OCR system specialized in extracting financial transaction data.

    **TASK:** Extract all transaction information from this image and return structured JSON.

    **EXTRACTION RULES:**
    1. Extract ALL transactions/line items visible
    2. Automatically categorize using predefined categories
    3. Extract dates in YYYY-MM-DD format
    4. Provide confidence scores for each extraction

    **OUTPUT FORMAT (JSON only):**
    {
        "transactions": [
            {
                "description": "Item description",
                "amount": 15.99,
                "date": "2024-01-15",
                "category": "FOOD_DINING",
                "merchant": "Store name",
                "confidence": 0.95
            }
        ],
        "document_type": "receipt",
        "processing_confidence": 0.88
    }
    """
    print(sample_ocr_prompt)
    print("```")


def show_integration_examples():
    """Show how to integrate AI features in frontend"""
    print("\n🌐 Frontend Integration Examples")
    print("=" * 35)
    
    print("\n📱 React Component Example:")
    print("```jsx")
    react_example = """
// OCR Upload Component
import React, { useState } from 'react';

function ReceiptUpload() {
  const [processing, setProcessing] = useState(false);
  const [ocrResult, setOcrResult] = useState(null);

  const handleFileUpload = async (file) => {
    setProcessing(true);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      // Step 1: Process with OCR
      const ocrResponse = await fetch('/api/ai/ocr/process', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      
      const ocrData = await ocrResponse.json();
      setOcrResult(ocrData);
      
      // Step 2: Show user for verification
      // (User can edit transactions here)
      
    } catch (error) {
      console.error('OCR processing failed:', error);
    } finally {
      setProcessing(false);
    }
  };

  const confirmTransactions = async () => {
    // Step 3: Create transactions
    const response = await fetch('/api/ai/transactions/bulk', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        transactions: ocrResult.transactions,
        source: 'ocr',
        verify_before_save: false
      })
    });
    
    const result = await response.json();
    console.log(`Created ${result.created_count} transactions`);
  };

  return (
    <div>
      <input 
        type="file" 
        accept="image/*" 
        onChange={(e) => handleFileUpload(e.target.files[0])}
        disabled={processing}
      />
      {processing && <div>Processing receipt...</div>}
      {ocrResult && (
        <div>
          <h3>Found {ocrResult.transactions.length} transactions</h3>
          <button onClick={confirmTransactions}>Add to Account</button>
        </div>
      )}
    </div>
  );
}
"""
    print(react_example)
    print("```")
    
    print("\n💡 AI Insights Component:")
    print("```jsx")
    insights_example = """
// AI Insights Dashboard
function AIInsightsDashboard() {
  const [analysis, setAnalysis] = useState(null);
  
  useEffect(() => {
    // Get AI analysis
    fetch('/api/ai/analyze?period_days=30', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => res.json())
    .then(setAnalysis);
  }, []);

  return (
    <div>
      {analysis && (
        <>
          <div className="summary">
            <h2>Financial Health Summary</h2>
            <p>{analysis.summary}</p>
            <div>Confidence: {(analysis.confidence_score * 100).toFixed(0)}%</div>
          </div>
          
          <div className="recommendations">
            <h3>Recommendations</h3>
            {analysis.recommendations.map((rec, i) => (
              <div key={i} className={`recommendation priority-${rec.priority}`}>
                <h4>{rec.title}</h4>
                <p>{rec.description}</p>
                {rec.potential_savings && (
                  <div>Potential Savings: ${rec.potential_savings}/month</div>
                )}
                <ul>
                  {rec.action_items.map((item, j) => (
                    <li key={j}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          
          <div className="insights">
            <h3>Spending Insights</h3>
            {analysis.insights.map((insight, i) => (
              <div key={i} className={`insight severity-${insight.severity}`}>
                <h4>{insight.title}</h4>
                <p>{insight.description}</p>
                {insight.metric_value && (
                  <div>{insight.metric_value} {insight.metric_unit}</div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
"""
    print(insights_example)
    print("```")


async def main():
    """Run complete demonstration"""
    # Demonstrate OCR workflow
    await demonstrate_ocr_workflow()
    
    # Show prompt engineering
    demonstrate_prompt_engineering()
    
    # Show integration examples
    show_integration_examples()
    
    print("\n🎉 OCR Workflow Demonstration Complete!")
    print("\n📋 Next Steps:")
    print("  1. Set up Gemini API key in environment")
    print("  2. Test with real receipt images")
    print("  3. Integrate OCR upload in frontend")
    print("  4. Add user verification interface")
    print("  5. Monitor AI API usage and costs")


if __name__ == "__main__":
    asyncio.run(main()) 