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
            
            # Prepare data context
            total_spending = sum(user_spending.values())
            total_budget = daily_budget * period_days
            total_income = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'income')
            
            # Create comprehensive prompt
            prompt = cls._create_financial_analysis_prompt(
                user_spending, daily_budget, goals, transactions, period_days
            )
            
            response = model.generate_content(prompt)
            
            # Parse structured response
            try:
                analysis_data = json.loads(response.text)
                return AIAnalysisResponse(**analysis_data)
            except json.JSONDecodeError:
                # If JSON parsing fails, create structured response from text
                return cls._parse_text_response(response.text, user_spending, daily_budget)
                
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return cls._generate_basic_analysis(user_spending, daily_budget, goals, transactions, period_days)

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
        
        return f"""
        You are a professional financial advisor AI. Analyze the user's financial data and provide structured insights.

        **USER FINANCIAL DATA:**
        - Daily Budget: ${daily_budget:.2f}
        - Period: {period_days} days
        - Total Budget: ${total_budget:.2f}
        - Total Spending: ${total_spending:.2f}
        - Total Income: ${total_income:.2f}
        
        **SPENDING BY CATEGORY:**
        {json.dumps(user_spending, indent=2)}
        
        **FINANCIAL GOALS:**
        {json.dumps(goals, indent=2)}
        
        **RECENT TRANSACTIONS (last 10):**
        {json.dumps(transactions[-10:], indent=2, default=str)}

        **ANALYSIS REQUIREMENTS:**
        1. Provide 3-5 personalized recommendations with specific action items
        2. Generate 3-5 data-driven insights about spending patterns
        3. Include potential savings estimates where applicable
        4. Prioritize recommendations by impact and urgency
        5. Consider user's goals and deadlines in recommendations

        **OUTPUT FORMAT (JSON):**
        {{
            "recommendations": [
                {{
                    "title": "Brief recommendation title",
                    "description": "Detailed explanation and reasoning",
                    "type": "budget_optimization|category_reduction|savings_increase|goal_acceleration|spending_pattern",
                    "priority": "high|medium|low",
                    "potential_savings": 150.00,
                    "action_items": ["Specific step 1", "Specific step 2"],
                    "category_focus": "FOOD_DINING|TRANSPORTATION|etc (optional)"
                }}
            ],
            "insights": [
                {{
                    "insight_type": "trend|pattern|comparison",
                    "title": "Brief insight title",
                    "description": "Detailed insight explanation",
                    "metric_value": 25.5,
                    "metric_unit": "percent|dollars|days",
                    "trend_direction": "up|down|stable",
                    "severity": "low|medium|high"
                }}
            ],
            "summary": "2-3 sentence overall financial health summary",
            "confidence_score": 0.85
        }}

        **GUIDELINES:**
        - Be specific and actionable in recommendations
        - Use actual numbers from the data
        - Consider seasonal patterns and user behavior
        - Prioritize high-impact, achievable changes
        - Be encouraging but honest about financial challenges
        - Focus on practical, implementable advice
        
        Respond with ONLY the JSON object, no additional text.
        """

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
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Convert image data to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Create OCR prompt
            prompt = cls._create_ocr_prompt()
            
            response = model.generate_content([prompt, image])
            
            # Parse the response
            try:
                ocr_data = json.loads(response.text)
                return cls._validate_ocr_result(ocr_data, response.text)
            except json.JSONDecodeError:
                # Try to extract structured data from text response
                return cls._parse_ocr_text_response(response.text)
                
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
        You are an expert OCR system specialized in extracting financial transaction data from receipts, bank statements, and financial documents.

        **TASK:** Extract all transaction information from this image and return structured JSON data.

        **EXPECTED DOCUMENT TYPES:**
        - Receipts (store, restaurant, gas station, etc.)
        - Bank statements
        - Credit card statements
        - Invoice documents
        - Expense reports

        **EXTRACTION RULES:**
        1. Extract ALL transactions/line items visible
        2. For receipts: extract individual items if detailed, or total if summary
        3. For statements: extract each transaction line
        4. Automatically categorize using these categories: {categories}
        5. Extract dates in YYYY-MM-DD format
        6. Extract amounts as positive decimal numbers
        7. Identify merchant/vendor names when possible
        8. Provide confidence scores for each extraction

        **OUTPUT FORMAT (JSON only):**
        {{
            "transactions": [
                {{
                    "description": "Item or transaction description",
                    "amount": 15.99,
                    "date": "2024-01-15",
                    "category": "FOOD_DINING",
                    "merchant": "Starbucks",
                    "confidence": 0.95
                }}
            ],
            "total_amount": 45.97,
            "document_type": "receipt|bank_statement|credit_statement|invoice|other",
            "processing_confidence": 0.88,
            "raw_text": "Complete extracted text for reference",
            "warnings": ["Any issues or uncertainties"]
        }}

        **GUIDELINES:**
        - If amount is unclear, estimate based on context
        - If date is missing, use today's date with low confidence
        - If category is uncertain, use MISCELLANEOUS
        - Include tax, tips, and fees as separate line items when detailed
        - For unclear text, note in warnings but still attempt extraction
        - Confidence should reflect OCR clarity and data certainty

        **RESPOND WITH ONLY THE JSON OBJECT, NO ADDITIONAL TEXT.**
        """

    @classmethod
    def _validate_ocr_result(cls, ocr_data: dict, raw_text: str) -> OCRResult:
        """Validate and structure OCR result"""
        
        transactions = []
        total_amount = Decimal('0')
        
        for item in ocr_data.get('transactions', []):
            try:
                # Validate and create transaction item
                transaction = OCRTransactionItem(
                    description=item.get('description', 'Unknown transaction'),
                    amount=Decimal(str(item.get('amount', 0))),
                    date=datetime.strptime(item.get('date', str(date.today())), '%Y-%m-%d').date(),
                    category=ExpenseCategory(item.get('category', 'MISCELLANEOUS')),
                    merchant=item.get('merchant'),
                    confidence=float(item.get('confidence', 0.5))
                )
                transactions.append(transaction)
                total_amount += transaction.amount
            except Exception as e:
                logger.warning(f"Failed to parse OCR transaction item: {e}")
                continue
        
        return OCRResult(
            transactions=transactions,
            total_amount=total_amount,
            document_type=ocr_data.get('document_type', 'unknown'),
            processing_confidence=float(ocr_data.get('processing_confidence', 0.5)),
            raw_text=raw_text,
            warnings=ocr_data.get('warnings', [])
        )

    @classmethod
    def _parse_ocr_text_response(cls, text: str) -> OCRResult:
        """Parse OCR response when JSON parsing fails"""
        
        # Basic text parsing fallback
        lines = text.split('\n')
        transactions = []
        
        # Simple pattern matching for amounts
        import re
        amount_pattern = r'\$?(\d+\.?\d*)'
        
        for line in lines:
            amounts = re.findall(amount_pattern, line)
            if amounts and line.strip():
                try:
                    amount = Decimal(amounts[-1])  # Take the last amount found
                    if amount > 0:
                        transactions.append(OCRTransactionItem(
                            description=line.strip()[:100],
                            amount=amount,
                            date=date.today(),
                            category=cls._fallback_categorize_transaction(line),
                            confidence=0.3
                        ))
                except:
                    continue
        
        total_amount = sum(t.amount for t in transactions)
        
        return OCRResult(
            transactions=transactions,
            total_amount=total_amount,
            document_type="unknown",
            processing_confidence=0.3,
            raw_text=text,
            warnings=["Failed to parse structured data, used text parsing fallback"]
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
            "You are a personal financial advisor AI assistant. Answer the user's question using their financial data.",
            f"\n**USER QUESTION:** {request.user_query}\n"
        ]
        
        if request.include_budget and user_data.get('daily_budget'):
            context_parts.append(f"**DAILY BUDGET:** ${user_data['daily_budget']:.2f}")
        
        if request.include_transactions and user_data.get('transactions'):
            transactions = user_data['transactions'][-20:]  # Last 20 transactions
            context_parts.append(f"**RECENT TRANSACTIONS:**\n{json.dumps(transactions, indent=2, default=str)}")
        
        if request.include_goals and user_data.get('goals'):
            context_parts.append(f"**FINANCIAL GOALS:**\n{json.dumps(user_data['goals'], indent=2, default=str)}")
        
        context_parts.extend([
            "\n**INSTRUCTIONS:**",
            "- Provide specific, actionable advice based on the user's actual data",
            "- Use concrete numbers and examples from their transactions",
            "- Be encouraging but realistic about financial challenges",
            "- Suggest specific tools or strategies they can implement",
            "- If the question is unclear, ask for clarification",
            "- Keep responses concise but comprehensive"
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