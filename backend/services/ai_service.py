from typing import Optional, List, Dict, Any, Union
import re
import json
import base64
from decimal import Decimal
from datetime import date, datetime, timedelta
import logging
import google.generativeai as genai
from PIL import Image
import io
import PyPDF2
from pdf2image import convert_from_bytes

from models.transaction import ExpenseCategory, TransactionType
from models.goal import Goal
from config import settings
from schemas.ai import (
    FinancialRecommendation, SpendingInsight, AIAnalysisResponse,
    OCRResult, OCRTransactionItem, RecommendationType, RecommendationPriority,
    AIPromptRequest, AIPromptResponse
)

# Configure Gemini
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)

logger = logging.getLogger(__name__)


class AIService:
    """Enhanced AI service using Gemini LLM for financial analysis and OCR"""
    
    # Simple rate limiting - track daily API calls
    _daily_api_calls = 0
    _last_reset_date = date.today()
    _max_daily_calls = 40  # Stay under the 50 limit
    
    @classmethod
    def _can_make_api_call(cls) -> bool:
        """Check if we can make another API call today"""
        today = date.today()
        
        # Reset counter if it's a new day
        if today > cls._last_reset_date:
            cls._daily_api_calls = 0
            cls._last_reset_date = today
        
        # Check if we're under the limit
        if cls._daily_api_calls >= cls._max_daily_calls:
            logger.warning(f"Daily Gemini API limit reached ({cls._max_daily_calls}), using fallback methods")
            return False
        
        return True
    
    @classmethod
    def _record_api_call(cls):
        """Record that we made an API call"""
        cls._daily_api_calls += 1
    
    # Keywords mapping for fallback categorization
    CATEGORY_KEYWORDS = {
        ExpenseCategory.FOOD_DINING: [
            'restaurant', 'cafe', 'pizza', 'burger', 'starbucks', 'mcdonalds',
            'dining', 'takeout', 'delivery', 'uber eats', 'doordash', 'grubhub'
        ],
        ExpenseCategory.GROCERIES: [
            'grocery', 'supermarket', 'walmart', 'target', 'costco', 'safeway',
            'kroger', 'whole foods', 'trader joes', 'food market'
        ],
        ExpenseCategory.TRANSPORTATION: [
            'gas', 'fuel', 'uber', 'lyft', 'taxi', 'bus', 'train', 'metro',
            'parking', 'toll', 'car wash', 'auto', 'vehicle'
        ],
        ExpenseCategory.SHOPPING: [
            'amazon', 'ebay', 'mall', 'store', 'shop', 'clothing', 'electronics',
            'best buy', 'apple store', 'nike', 'adidas'
        ],
        ExpenseCategory.ENTERTAINMENT: [
            'movie', 'cinema', 'netflix', 'spotify', 'gaming', 'concert',
            'theater', 'entertainment', 'streaming', 'subscription'
        ],
        ExpenseCategory.BILLS_UTILITIES: [
            'electric', 'water', 'gas bill', 'internet', 'phone', 'rent',
            'mortgage', 'insurance', 'utility', 'bill'
        ],
        ExpenseCategory.HEALTHCARE: [
            'doctor', 'hospital', 'pharmacy', 'medical', 'health', 'dentist',
            'clinic', 'prescription', 'cvs', 'walgreens'
        ],
        ExpenseCategory.EDUCATION: [
            'school', 'university', 'course', 'book', 'tuition', 'education',
            'learning', 'training', 'certification'
        ],
        ExpenseCategory.TRAVEL: [
            'hotel', 'flight', 'airline', 'vacation', 'travel', 'booking',
            'airbnb', 'rental car', 'trip'
        ],
        ExpenseCategory.FITNESS: [
            'gym', 'fitness', 'workout', 'sports', 'yoga', 'trainer',
            'athletic', 'exercise', 'health club'
        ],
        ExpenseCategory.PERSONAL_CARE: [
            'salon', 'haircut', 'beauty', 'cosmetics', 'spa', 'barber',
            'nail', 'skincare', 'personal care'
        ],
        ExpenseCategory.GIFTS_DONATIONS: [
            'gift', 'donation', 'charity', 'present', 'birthday', 'wedding',
            'holiday', 'christmas', 'valentine'
        ],
        ExpenseCategory.BUSINESS: [
            'office', 'business', 'work', 'professional', 'conference',
            'meeting', 'supplies', 'equipment'
        ]
    }

    @classmethod
    def _get_gemini_model(cls):
        """Get configured Gemini model"""
        try:
            return genai.GenerativeModel(settings.gemini_model)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            return None

    @classmethod
    def categorize_transaction(cls, description: str, amount: float = None) -> ExpenseCategory:
        """
        Enhanced transaction categorization using Gemini LLM with fallback to keyword matching
        """
        if not description:
            return ExpenseCategory.MISCELLANEOUS
        
        # Check if we can make API call
        if not cls._can_make_api_call():
            logger.info("Using fallback categorization due to rate limiting")
            return cls._fallback_categorize_transaction(description)
        
        # Try Gemini categorization first
        try:
            model = cls._get_gemini_model()
            if model:
                prompt = f"""
                Categorize this transaction into one of these categories:
                {', '.join([cat.value for cat in ExpenseCategory])}
                
                Transaction: "{description}"
                Amount: ${amount if amount else 'unknown'}
                
                Respond with ONLY the category name (e.g., FOOD_DINING).
                Consider the context and merchant type carefully.
                """
                
                response = model.generate_content(prompt)
                cls._record_api_call()  # Record successful API call
                category_name = response.text.strip().upper()
                
                # Validate response
                for category in ExpenseCategory:
                    if category.value == category_name:
                        return category
        except Exception as e:
            logger.warning(f"Gemini categorization failed, using fallback: {e}")
        
        # Fallback to keyword matching
        return cls._fallback_categorize_transaction(description)

    @classmethod
    def _fallback_categorize_transaction(cls, description: str) -> ExpenseCategory:
        """Fallback keyword-based categorization"""
        if not description:
            return ExpenseCategory.MISCELLANEOUS
        
        description_lower = description.lower()
        category_scores = {}
        
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in description_lower:
                    if keyword.lower() == description_lower:
                        score += 10
                    else:
                        score += 1
            
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])[0]
            return best_category
        
        return ExpenseCategory.MISCELLANEOUS

    @classmethod
    def generate_enhanced_analysis(
        cls,
        user_spending: Dict[str, float],
        daily_budget: float,
        goals: List[Dict[str, Any]],
        transactions: List[Dict[str, Any]],
        period_days: int = 30
    ) -> AIAnalysisResponse:
        """Generate comprehensive AI-powered financial analysis using Gemini"""
        
        try:
            model = cls._get_gemini_model()
            if not model:
                # Fallback to basic analysis
                return cls._generate_basic_analysis(user_spending, daily_budget, goals, transactions, period_days)
            
            # Create comprehensive prompt
            prompt = cls._create_financial_analysis_prompt(
                user_spending, daily_budget, goals, transactions, period_days
            )
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean the response text to ensure it's valid JSON
            response_text = cls._clean_json_response(response_text)
            
            # Parse structured response
            try:
                analysis_data = json.loads(response_text)
                # Validate the structure before creating the response
                validated_data = cls._validate_analysis_data(analysis_data)
                return AIAnalysisResponse(**validated_data)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {e}. Response: {response_text[:500]}...")
                # If JSON parsing fails, create structured response from text
                return cls._parse_text_response(response_text, user_spending, daily_budget)
                
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return cls._generate_basic_analysis(user_spending, daily_budget, goals, transactions, period_days)

    @classmethod
    def _clean_json_response(cls, response_text: str) -> str:
        """Clean the response text to ensure it's valid JSON"""
        # Remove markdown code blocks if present
        response_text = re.sub(r'^```(?:json)?\s*', '', response_text, flags=re.MULTILINE)
        response_text = re.sub(r'\s*```$', '', response_text, flags=re.MULTILINE)
        
        # Remove any leading/trailing whitespace
        response_text = response_text.strip()
        
        # Ensure it starts with { and ends with }
        if not response_text.startswith('{'):
            # Try to find the first { character
            start_idx = response_text.find('{')
            if start_idx != -1:
                response_text = response_text[start_idx:]
        
        if not response_text.endswith('}'):
            # Try to find the last } character
            end_idx = response_text.rfind('}')
            if end_idx != -1:
                response_text = response_text[:end_idx + 1]
        
        return response_text

    @classmethod
    def _validate_analysis_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize the analysis data"""
        validated = {
            "recommendations": [],
            "insights": [],
            "summary": data.get("summary", "Financial analysis completed."),
            "confidence_score": max(0.0, min(1.0, float(data.get("confidence_score", 0.7))))
        }
        
        # Validate recommendations
        for rec in data.get("recommendations", []):
            if isinstance(rec, dict) and rec.get("title") and rec.get("description"):
                validated_rec = {
                    "title": str(rec["title"])[:60],  # Truncate to max length
                    "description": str(rec["description"])[:200],
                    "type": rec.get("type", "budget_optimization"),
                    "priority": rec.get("priority", "medium"),
                    "potential_savings": float(rec.get("potential_savings", 0.0)),
                    "action_items": rec.get("action_items", [])[:5],  # Max 5 items
                }
                if rec.get("category_focus"):
                    validated_rec["category_focus"] = rec["category_focus"]
                validated["recommendations"].append(validated_rec)
        
        # Validate insights
        for insight in data.get("insights", []):
            if isinstance(insight, dict) and insight.get("title") and insight.get("description"):
                validated_insight = {
                    "insight_type": insight.get("insight_type", "pattern"),
                    "title": str(insight["title"])[:50],
                    "description": str(insight["description"])[:150],
                    "trend_direction": insight.get("trend_direction", "stable"),
                    "severity": insight.get("severity", "medium")
                }
                if insight.get("metric_value") is not None:
                    validated_insight["metric_value"] = float(insight["metric_value"])
                if insight.get("metric_unit"):
                    validated_insight["metric_unit"] = insight["metric_unit"]
                validated["insights"].append(validated_insight)
        
        return validated

    @classmethod
    def _create_financial_analysis_prompt(
        cls,
        user_spending: Dict[str, float],
        daily_budget: float,
        goals: List[Dict[str, Any]],
        transactions: List[Dict[str, Any]],
        period_days: int
    ) -> str:
        """Create structured prompt for Gemini financial analysis"""
        
        total_spending = sum(user_spending.values())
        total_budget = daily_budget * period_days
        total_income = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'income')
        
        return f"""CRITICAL INSTRUCTION: You MUST respond with VALID JSON ONLY. No markdown, no explanations, no code blocks, no backticks. Just pure JSON.

FINANCIAL DATA ANALYSIS REQUEST:
Daily Budget: ${daily_budget:.2f}
Period: {period_days} days  
Total Budget: ${total_budget:.2f}
Total Spending: ${total_spending:.2f}
Total Income: ${total_income:.2f}

SPENDING DATA: {json.dumps(user_spending)}
GOALS DATA: {json.dumps(goals)}
RECENT TRANSACTIONS: {json.dumps(transactions[-5:], default=str)}

REQUIRED JSON SCHEMA - YOU MUST FOLLOW THIS EXACTLY:
{{
  "recommendations": [
    {{
      "title": "string (max 60 chars)",
      "description": "string (max 200 chars, actionable advice)",
      "type": "budget_optimization",
      "priority": "high",
      "potential_savings": 0.0,
      "action_items": ["string", "string"],
      "category_focus": "FOOD_DINING"
    }}
  ],
  "insights": [
    {{
      "insight_type": "pattern",
      "title": "string (max 50 chars)",
      "description": "string (max 150 chars)",
      "metric_value": 0.0,
      "metric_unit": "dollars",
      "trend_direction": "up",
      "severity": "medium"
    }}
  ],
  "summary": "string (max 150 chars)",
  "confidence_score": 0.85
}}

MANDATORY FIELD VALUES:
- type: ONLY "budget_optimization", "category_reduction", "savings_increase", "goal_acceleration", or "spending_pattern"
- priority: ONLY "high", "medium", or "low"  
- insight_type: ONLY "trend", "pattern", or "comparison"
- metric_unit: ONLY "dollars", "percent", or "days"
- trend_direction: ONLY "up", "down", or "stable"
- severity: ONLY "low", "medium", or "high"
- category_focus: ONLY ExpenseCategory values like "FOOD_DINING", "TRANSPORTATION", etc.

ANALYSIS RULES:
1. Generate 2-4 recommendations with specific dollar amounts
2. Generate 2-4 insights with real metrics from the data
3. All numbers must be realistic based on provided data
4. Use actual spending amounts in calculations
5. Action items must be specific and actionable
6. Summary must reflect actual financial situation

RESPONSE FORMAT: Start immediately with {{ and end with }}. NO OTHER TEXT ALLOWED."""

    @classmethod
    def _generate_basic_analysis(
        cls,
        user_spending: Dict[str, float],
        daily_budget: float,
        goals: List[Dict[str, Any]],
        transactions: List[Dict[str, Any]],
        period_days: int
    ) -> AIAnalysisResponse:
        """Generate basic analysis when Gemini is unavailable"""
        
        recommendations = []
        insights = []
        
        total_spending = sum(user_spending.values())
        total_budget = daily_budget * period_days
        
        # Basic recommendations
        if total_spending > total_budget:
            overspend = total_spending - total_budget
            recommendations.append(FinancialRecommendation(
                title="Reduce Overall Spending",
                description=f"You overspent by ${overspend:.2f} this period. Focus on cutting discretionary expenses.",
                type=RecommendationType.BUDGET_OPTIMIZATION,
                priority=RecommendationPriority.HIGH,
                potential_savings=Decimal(str(overspend * 0.3)),
                action_items=["Review all expenses", "Identify non-essential purchases", "Set spending alerts"]
            ))
        
        # Category-specific recommendations
        for category, amount in user_spending.items():
            if amount > total_budget * 0.25:  # More than 25% of budget
                recommendations.append(FinancialRecommendation(
                    title=f"Optimize {category.replace('_', ' ').title()} Spending",
                    description=f"This category represents ${amount:.2f} of your spending. Consider ways to reduce it.",
                    type=RecommendationType.CATEGORY_REDUCTION,
                    priority=RecommendationPriority.MEDIUM,
                    potential_savings=Decimal(str(amount * 0.2)),
                    action_items=["Track spending in this category", "Look for alternatives", "Set category limits"],
                    category_focus=ExpenseCategory(category) if hasattr(ExpenseCategory, category) else None
                ))
        
        # Basic insights
        if user_spending:
            top_category = max(user_spending.items(), key=lambda x: x[1])
            insights.append(SpendingInsight(
                insight_type="pattern",
                title="Top Spending Category",
                description=f"Your highest spending is in {top_category[0].replace('_', ' ').title()}",
                metric_value=top_category[1],
                metric_unit="dollars",
                trend_direction="stable",
                severity="medium" if top_category[1] > total_budget * 0.3 else "low"
            ))
        
        budget_utilization = (total_spending / total_budget * 100) if total_budget > 0 else 0
        insights.append(SpendingInsight(
            insight_type="comparison",
            title="Budget Utilization",
            description=f"You've used {budget_utilization:.1f}% of your budget this period",
            metric_value=budget_utilization,
            metric_unit="percent",
            trend_direction="up" if budget_utilization > 90 else "stable",
            severity="high" if budget_utilization > 100 else "medium" if budget_utilization > 80 else "low"
        ))
        
        summary = f"You've spent ${total_spending:.2f} out of ${total_budget:.2f} budget. "
        if budget_utilization > 100:
            summary += "Focus on reducing expenses to get back on track."
        elif budget_utilization < 80:
            summary += "Great job staying under budget!"
        else:
            summary += "You're using your budget efficiently."
        
        return AIAnalysisResponse(
            recommendations=recommendations,
            insights=insights,
            summary=summary,
            confidence_score=0.7
        )

    @classmethod
    def _parse_text_response(cls, text: str, user_spending: Dict[str, float], daily_budget: float) -> AIAnalysisResponse:
        """Parse text response when JSON parsing fails"""
        # Basic fallback parsing
        recommendations = [FinancialRecommendation(
            title="AI Analysis Available",
            description=text[:200] + "..." if len(text) > 200 else text,
            type=RecommendationType.BUDGET_OPTIMIZATION,
            priority=RecommendationPriority.MEDIUM,
            action_items=["Review the AI analysis", "Implement suggested changes"]
        )]
        
        return AIAnalysisResponse(
            recommendations=recommendations,
            insights=[],
            summary="AI analysis completed. Review recommendations for details.",
            confidence_score=0.6
        )

    @classmethod
    async def process_receipt_ocr(cls, image_data: bytes, filename: str) -> OCRResult:
        """Process receipt/document using Gemini Vision for OCR and transaction extraction"""
        
        try:
            if not cls._can_make_api_call():
                return OCRResult(
                    transactions=[],
                    total_amount=Decimal('0'),
                    document_type="unknown",
                    processing_confidence=0.0,
                    raw_text="Daily API limit reached",
                    warnings=["Daily API limit reached, please try again later"]
                )
                
            cls._record_api_call()
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Determine file type and process accordingly
            is_pdf = filename.lower().endswith('.pdf')
            images = []
            
            if is_pdf:
                # Process PDF file
                try:
                    # First try to extract text directly from PDF
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(image_data))
                    raw_text = ""
                    for page in pdf_reader.pages:
                        raw_text += page.extract_text() + "\n"
                    
                    # If PDF has extractable text, use it with Gemini
                    if raw_text.strip():
                        logger.info("PDF contains extractable text, processing with text analysis")
                        response = model.generate_content([
                            cls._create_pdf_text_ocr_prompt(), 
                            f"PDF Content:\n{raw_text}"
                        ])
                        response_text = response.text.strip()
                    else:
                        # Convert PDF to images for OCR if no text found
                        logger.info("PDF has no extractable text, converting to images for OCR")
                        images = convert_from_bytes(image_data, dpi=200, first_page=1, last_page=3)  # Process first 3 pages max
                        if not images:
                            raise Exception("Could not convert PDF to images")
                        
                        # Use the first page for OCR (can be extended to process multiple pages)
                        main_image = images[0]
                        prompt = cls._create_ocr_prompt()
                        response = model.generate_content([prompt, main_image])
                        response_text = response.text.strip()
                        
                except Exception as e:
                    logger.error(f"PDF processing failed: {e}")
                    return OCRResult(
                        transactions=[],
                        total_amount=Decimal('0'),
                        document_type="pdf",
                        processing_confidence=0.0,
                        raw_text=f"PDF processing failed: {str(e)}",
                        warnings=[f"PDF processing failed: {str(e)}"]
                    )
            else:
                # Process regular image file
                image = Image.open(io.BytesIO(image_data))
                prompt = cls._create_ocr_prompt()
                response = model.generate_content([prompt, image])
                response_text = response.text.strip()
            
            logger.info(f"Raw OCR response: {response_text[:500]}...")  # Log first 500 chars
            
            # Clean the response text - remove markdown formatting if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            # Parse the response
            try:
                ocr_data = json.loads(response_text)
                logger.info(f"Successfully parsed OCR JSON data")
                return cls._validate_ocr_result(ocr_data, response_text)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing failed: {e}, attempting fallback parsing")
                # Try to extract structured data from text response
                return cls._parse_ocr_text_response(response_text)
                
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            return OCRResult(
                transactions=[],
                total_amount=Decimal('0'),
                document_type="unknown",
                processing_confidence=0.0,
                raw_text=str(e),
                warnings=[f"OCR processing failed: {str(e)}"]
            )

    @classmethod
    def _create_ocr_prompt(cls) -> str:
        """Create structured prompt for OCR transaction extraction"""
        
        categories = ', '.join([cat.value for cat in ExpenseCategory])
        
        return f"""
IMPORTANT: You are an expert OCR system. Analyze the receipt/document image and extract transaction data. Return ONLY valid JSON - no markdown, no explanations, no code blocks.

TASK: Extract structured transaction data from this financial document.

EXTRACTION RULES:
1. READ the image carefully - identify all line items with descriptions and amounts
2. For retail receipts: Extract each product/service line item separately
3. Match each description with its corresponding price
4. Extract the correct transaction date from the document (look for date stamps)
5. Categorize items appropriately from: {categories}
6. Identify any merchant/store name from headers or footers
7. Calculate or use the provided total amount

RECEIPT PARSING PRIORITY:
- Line items (products/services) with individual prices
- Transaction date (usually at top or bottom)
- Merchant name (store/business name)
- Total amount
- Payment method if visible

JSON STRUCTURE (return exactly this format):
{{
  "transactions": [
    {{
      "description": "Product or service name (clean, readable)",
      "amount": 25.50,
      "date": "2024-01-15",
      "category": "SHOPPING",
      "merchant": "Store Name",
      "confidence": 0.95
    }}
  ],
  "total_amount": 363.99,
  "document_type": "receipt",
  "processing_confidence": 0.95,
  "raw_text": "All extracted text from document",
  "warnings": []
}}

CATEGORIES (use exact values):
- SHOPPING: Clothing, electronics, general retail
- FOOD_DINING: Restaurants, fast food, cafes
- GROCERIES: Supermarkets, food stores
- TRANSPORTATION: Gas, parking, rideshare
- ENTERTAINMENT: Movies, games, subscriptions
- BILLS_UTILITIES: Phone, internet, electricity
- HEALTHCARE: Medical, pharmacy, dental
- MISCELLANEOUS: When category unclear

CRITICAL INSTRUCTIONS:
- Return ONLY the JSON object
- No ```json``` markdown formatting
- No additional text before or after JSON
- Ensure all JSON syntax is correct
- Use double quotes for all strings
- Include decimal amounts (e.g., 25.50, not 25.5)
- Date format: YYYY-MM-DD
- If date unclear, use document date or current date

EXAMPLE VALID RESPONSE:
{{"transactions":[{{"description":"T-Shirt","amount":25.50,"date":"2024-01-15","category":"SHOPPING","merchant":"Retail Store","confidence":0.95}}],"total_amount":25.50,"document_type":"receipt","processing_confidence":0.95,"raw_text":"Receipt content","warnings":[]}}
"""

    @classmethod
    def _create_pdf_text_ocr_prompt(cls) -> str:
        """Create structured prompt for PDF text extraction and transaction analysis"""
        
        categories = ', '.join([cat.value for cat in ExpenseCategory])
        
        return f"""
IMPORTANT: You are an expert financial document analyzer. Analyze the PDF text content and extract transaction data. Return ONLY valid JSON - no markdown, no explanations, no code blocks.

TASK: Extract structured transaction data from this PDF financial document text.

EXTRACTION RULES:
1. READ the text carefully - identify all transactions, line items, or financial entries
2. For statements/invoices: Extract each transaction line separately
3. For receipts: Extract each product/service line item separately
4. Match descriptions with corresponding amounts
5. Extract transaction dates (look for date patterns in the text)
6. Categorize items appropriately from: {categories}
7. Identify merchant/business names from headers or content
8. Calculate totals or use provided amounts

PDF TEXT PARSING PRIORITY:
- Transaction entries with dates and amounts
- Line items with descriptions and prices
- Merchant/business information
- Statement periods or transaction dates
- Total amounts and subtotals

JSON STRUCTURE (return exactly this format):
{{
  "transactions": [
    {{
      "description": "Transaction or item description (clean, readable)",
      "amount": 25.50,
      "date": "2024-01-15",
      "category": "SHOPPING",
      "merchant": "Business Name",
      "confidence": 0.95
    }}
  ],
  "total_amount": 363.99,
  "document_type": "pdf_statement",
  "processing_confidence": 0.95,
  "raw_text": "Key extracted text from PDF",
  "warnings": []
}}

CATEGORIES (use exact values):
- SHOPPING: Clothing, electronics, general retail
- FOOD_DINING: Restaurants, fast food, cafes
- GROCERIES: Supermarkets, food stores
- TRANSPORTATION: Gas, parking, rideshare
- ENTERTAINMENT: Movies, games, subscriptions
- BILLS_UTILITIES: Phone, internet, electricity
- HEALTHCARE: Medical, pharmacy, dental
- MISCELLANEOUS: When category unclear

CRITICAL INSTRUCTIONS:
- Return ONLY the JSON object
- No ```json``` markdown formatting
- No additional text before or after JSON
- Ensure all JSON syntax is correct
- Use double quotes for all strings
- Include decimal amounts (e.g., 25.50, not 25.5)
- Date format: YYYY-MM-DD
- If date unclear, use document date or current date
- Extract individual transactions, not summary totals
"""

    @classmethod
    def _validate_ocr_result(cls, ocr_data: dict, raw_text: str) -> OCRResult:
        """Validate and structure OCR result with enhanced error handling"""
        
        transactions = []
        total_amount = Decimal('0')
        warnings = []
        
        # Validate transactions list
        transactions_data = ocr_data.get('transactions', [])
        if not isinstance(transactions_data, list):
            warnings.append("Invalid transactions format, expected list")
            transactions_data = []
        
        for idx, item in enumerate(transactions_data):
            try:
                # Handle string amounts that might contain JSON artifacts
                raw_amount = item.get('amount', 0)
                if isinstance(raw_amount, str):
                    # Clean up string amounts that might have JSON formatting
                    raw_amount = re.sub(r'[^\d.]', '', raw_amount)
                    if not raw_amount:
                        raw_amount = '0'
                
                amount = Decimal(str(raw_amount))
                
                # Handle date parsing
                date_str = item.get('date', str(date.today()))
                try:
                    parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except:
                    try:
                        # Try alternative date formats
                        parsed_date = datetime.strptime(date_str, '%m-%d-%Y').date()
                    except:
                        parsed_date = date.today()
                        warnings.append(f"Invalid date format in transaction {idx + 1}, using today's date")
                
                # Handle category validation
                category_str = item.get('category', 'MISCELLANEOUS')
                try:
                    category = ExpenseCategory(category_str)
                except ValueError:
                    category = ExpenseCategory.MISCELLANEOUS
                    warnings.append(f"Invalid category '{category_str}' in transaction {idx + 1}, using MISCELLANEOUS")
                
                # Create transaction item
                transaction = OCRTransactionItem(
                    description=str(item.get('description', 'Unknown transaction'))[:200],  # Limit description length
                    amount=amount,
                    date=parsed_date,
                    category=category,
                    merchant=item.get('merchant'),
                    confidence=min(1.0, max(0.0, float(item.get('confidence', 0.5))))  # Clamp confidence between 0 and 1
                )
                transactions.append(transaction)
                total_amount += transaction.amount
                
            except Exception as e:
                warnings.append(f"Failed to parse transaction {idx + 1}: {str(e)}")
                logger.warning(f"Failed to parse OCR transaction item {idx}: {e}")
                continue
        
        # Validate total amount
        provided_total = ocr_data.get('total_amount', 0)
        try:
            provided_total_decimal = Decimal(str(provided_total))
            # Use provided total if it seems reasonable
            if abs(provided_total_decimal - total_amount) / max(provided_total_decimal, total_amount, Decimal('1')) < 0.1:
                total_amount = provided_total_decimal
            elif provided_total_decimal > 0:
                warnings.append(f"Total amount mismatch: calculated {total_amount}, provided {provided_total_decimal}")
        except:
            warnings.append("Invalid total amount format")
        
        # Combine warnings
        existing_warnings = ocr_data.get('warnings', [])
        if isinstance(existing_warnings, list):
            warnings.extend(existing_warnings)
        
        return OCRResult(
            transactions=transactions,
            total_amount=total_amount,
            document_type=ocr_data.get('document_type', 'unknown'),
            processing_confidence=min(1.0, max(0.0, float(ocr_data.get('processing_confidence', 0.5)))),
            raw_text=raw_text,
            warnings=warnings
        )

    @classmethod
    def _parse_ocr_text_response(cls, text: str) -> OCRResult:
        """Parse OCR response when JSON parsing fails - improved fallback"""
        
        logger.info(f"Attempting fallback text parsing on: {text[:200]}...")
        
        # Try to find JSON-like structure in the text
        import re
        
        # Look for potential JSON structures
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        json_matches = re.findall(json_pattern, text, re.DOTALL)
        
        for match in json_matches:
            try:
                ocr_data = json.loads(match)
                if 'transactions' in ocr_data:
                    logger.info("Found valid JSON structure in text")
                    return cls._validate_ocr_result(ocr_data, text)
            except:
                continue
        
        # If no JSON found, try to extract key information patterns
        transactions = []
        
        # Pattern for receipt items: description + amount
        item_patterns = [
            r'(\d+)\s*x\s*([^$\n]+)\s*\$?(\d+\.?\d*)',  # "1 x T-Shirt $25.50"
            r'([^$\n]+)\s*\$(\d+\.?\d*)',  # "T-Shirt $25.50"
            r'"([^"]+)"\s*[,:]\s*(\d+\.?\d*)',  # "T-Shirt": 25.50
        ]
        
        # Extract date if possible
        date_pattern = r'(\d{2}[-/]\d{2}[-/]\d{4})'
        date_matches = re.findall(date_pattern, text)
        extracted_date = date.today()
        
        if date_matches:
            try:
                # Convert date format
                date_str = date_matches[0].replace('-', '/').replace('/', '-')
                if len(date_str.split('-')[2]) == 4:  # YYYY format
                    extracted_date = datetime.strptime(date_str, '%m-%d-%Y').date()
                else:  # YY format  
                    year = int('20' + date_str.split('-')[2])
                    month, day = date_str.split('-')[0], date_str.split('-')[1]
                    extracted_date = datetime(year, int(month), int(day)).date()
            except:
                pass
        
        # Try each pattern
        for pattern in item_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    if len(match) == 3:  # quantity, description, amount
                        quantity, description, amount_str = match
                        description = f"{quantity} x {description.strip()}"
                        amount = Decimal(amount_str)
                    else:  # description, amount
                        description, amount_str = match
                        description = description.strip()
                        amount = Decimal(amount_str)
                    
                    if amount > 0:
                        transactions.append(OCRTransactionItem(
                            description=description[:100],
                            amount=amount,
                            date=extracted_date,
                            category=cls._fallback_categorize_transaction(description),
                            confidence=0.6
                        ))
                except Exception as e:
                    logger.debug(f"Failed to parse match {match}: {e}")
                    continue
        
        # If still no transactions found, try simple amount extraction
        if not transactions:
            amount_pattern = r'\$?(\d+\.?\d{2})'
            amounts = re.findall(amount_pattern, text)
            
            # Look for the largest amount as likely total
            if amounts:
                amounts = [Decimal(a) for a in amounts if Decimal(a) > 0]
                if amounts:
                    max_amount = max(amounts)
                    transactions.append(OCRTransactionItem(
                        description="Receipt transaction",
                        amount=max_amount,
                        date=extracted_date,
                        category=ExpenseCategory.MISCELLANEOUS,
                        confidence=0.4
                    ))
        
        total_amount = sum(t.amount for t in transactions) if transactions else Decimal('0')
        
        return OCRResult(
            transactions=transactions,
            total_amount=total_amount,
            document_type="receipt" if transactions else "unknown",
            processing_confidence=0.6 if transactions else 0.3,
            raw_text=text,
            warnings=["Failed to parse structured data, used enhanced text parsing fallback"]
        )

    @classmethod
    async def custom_ai_query(
        cls,
        request: AIPromptRequest,
        user_data: Dict[str, Any]
    ) -> AIPromptResponse:
        """Handle custom AI queries using Gemini with user's financial context"""
        
        try:
            model = cls._get_gemini_model()
            if not model:
                return AIPromptResponse(
                    response="AI service is currently unavailable. Please try again later.",
                    confidence=0.0,
                    data_sources=[],
                    suggestions=[]
                )
            
            # Build context prompt
            context_prompt = cls._create_context_prompt(request, user_data)
            
            response = model.generate_content(context_prompt)
            
            # Extract suggestions from response
            suggestions = cls._extract_suggestions(response.text)
            
            return AIPromptResponse(
                response=response.text,
                data_sources=cls._get_data_sources_used(request),
                suggestions=suggestions,
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Custom AI query failed: {e}")
            return AIPromptResponse(
                response=f"I encountered an error processing your request: {str(e)}",
                confidence=0.0,
                data_sources=[],
                suggestions=["Try rephrasing your question", "Check your internet connection"]
            )

    @classmethod
    def _create_context_prompt(cls, request: AIPromptRequest, user_data: Dict[str, Any]) -> str:
        """Create context-aware prompt for custom queries"""
        
        context_parts = [
            "You are a professional financial advisor AI. Provide clear, actionable advice based on user's financial data.",
            f"\nUSER QUESTION: {request.user_query}",
            ""
        ]
        
        if request.include_budget and user_data.get('daily_budget'):
            context_parts.append(f"DAILY BUDGET: ${user_data['daily_budget']:.2f}")
        
        if request.include_transactions and user_data.get('transactions'):
            transactions = user_data['transactions'][-15:]  # Last 15 transactions
            total_spent = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
            context_parts.append(f"RECENT SPENDING: ${total_spent:.2f}")
            context_parts.append(f"TRANSACTIONS: {json.dumps(transactions, default=str)}")
        
        if request.include_goals and user_data.get('goals'):
            goals_summary = []
            for goal in user_data['goals']:
                progress = (goal.get('current_amount', 0) / goal.get('target_amount', 1)) * 100
                goals_summary.append(f"{goal.get('title')}: {progress:.0f}% complete")
            context_parts.append(f"GOALS: {', '.join(goals_summary)}")
        
        context_parts.extend([
            "",
            "RESPONSE GUIDELINES:",
            "- Answer directly and specifically using their actual data",
            "- Include concrete numbers and calculations where relevant",
            "- Provide 2-3 actionable recommendations",
            "- Use bullet points for clear action items",
            "- Be encouraging but realistic",
            "- Keep response under 300 words",
            "- If data is insufficient, suggest what information would help"
        ])
        
        return "\n".join(context_parts)

    @classmethod
    def _extract_suggestions(cls, response_text: str) -> List[str]:
        """Extract actionable suggestions from AI response"""
        
        suggestions = []
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                suggestion = line.lstrip('-•* ').strip()
                if len(suggestion) > 10:  # Filter out very short items
                    suggestions.append(suggestion)
        
        return suggestions[:5]  # Limit to 5 suggestions

    @classmethod
    def _get_data_sources_used(cls, request: AIPromptRequest) -> List[str]:
        """Get list of data sources used in analysis"""
        
        sources = []
        if request.include_transactions:
            sources.append("Recent transactions")
        if request.include_goals:
            sources.append("Financial goals")
        if request.include_budget:
            sources.append("Budget information")
        
        return sources

    @classmethod
    def calculate_goal_progress(cls, goal: Goal, current_amount: Decimal) -> Dict[str, Any]:
        """Calculate progress toward a specific goal"""
        progress_percentage = (current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        remaining_amount = goal.target_amount - current_amount
        days_remaining = (goal.deadline - date.today()).days
        
        # Calculate daily savings needed
        daily_savings_needed = remaining_amount / days_remaining if days_remaining > 0 and remaining_amount > 0 else Decimal(0)
        
        return {
            "progress_percentage": float(progress_percentage),
            "remaining_amount": float(remaining_amount),
            "days_remaining": days_remaining,
            "daily_savings_needed": float(daily_savings_needed),
            "is_on_track": progress_percentage >= (1 - days_remaining / ((goal.deadline - goal.created_at.date()).days or 1)) * 100
        }

    # Legacy methods for backward compatibility
    @classmethod
    def generate_personalized_recommendations(
        cls,
        user_spending: Dict[str, float],
        daily_budget: float,
        goals: List[Dict[str, Any]]
    ) -> List[str]:
        """Legacy method - use generate_enhanced_analysis instead"""
        analysis = cls._generate_basic_analysis(user_spending, daily_budget, goals, [], 30)
        return [rec.description for rec in analysis.recommendations]

    @classmethod
    def generate_spending_insights(
        cls, 
        transactions: List[Dict[str, Any]], 
        daily_budget: float,
        period_days: int = 30
    ) -> List[str]:
        """Legacy method - use generate_enhanced_analysis instead"""
        user_spending = {}
        for t in transactions:
            if t.get('type') == 'expense' and t.get('category'):
                category = t['category']
                user_spending[category] = user_spending.get(category, 0) + t.get('amount', 0)
        
        analysis = cls._generate_basic_analysis(user_spending, daily_budget, [], transactions, period_days)
        return [insight.description for insight in analysis.insights] 