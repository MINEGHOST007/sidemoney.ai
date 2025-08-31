# Backend Features - Finance Tracker MVP (24-Hour Assignment)

## 🔐 Authentication
- **Google OAuth**: Simple Google sign-in integration
  - JWT token-based authentication
  - Basic session management
  - Automatic user creation on first login

## 📊 Core Data Models

### 1. User Model
```python
- id: UUID (Primary Key)
- email: String (from Google OAuth)
- name: String (from Google OAuth)
- avatar_url: String (from Google OAuth)
- monthly_income: Decimal
- preferred_spending_days: Array[String] (e.g., ["Friday", "Saturday"])
- daily_budget_multiplier: Decimal (higher on preferred days)
- current_amount: Decimal (default: 0)
- created_at: DateTime
- updated_at: DateTime
```

### 2. Transaction Model -operates on user'scurrent amount 
```python
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key → User)
- amount: Decimal
- type: Enum ("income", "expense")
- category: Enum (predefined categories)
- description: String
- date: Date
- created_at: DateTime
- updated_at: DateTime
```

### 3. Goal Model
```python
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key → User)
- title: String
- target_amount: Decimal
- deadline: Date
- created_at: DateTime
- updated_at: DateTime
```

## 📋 Predefined Categories (Enum)
```python
EXPENSE_CATEGORIES = [
    "FOOD_DINING",           # Restaurants, takeout
    "GROCERIES",             # Grocery shopping
    "TRANSPORTATION",        # Gas, public transport, ride-sharing
    "SHOPPING",              # Clothing, electronics, general shopping
    "ENTERTAINMENT",         # Movies, games, subscriptions
    "BILLS_UTILITIES",       # Rent, electricity, water, internet
    "HEALTHCARE",            # Medical, pharmacy, insurance
    "EDUCATION",             # Books, courses, tuition
    "TRAVEL",                # Hotels, flights, vacation
    "FITNESS",               # Gym, sports, health
    "PERSONAL_CARE",         # Haircuts, cosmetics
    "GIFTS_DONATIONS",       # Gifts, charity
    "BUSINESS",              # Work-related expenses
    "MISCELLANEOUS"          # Everything else
]
```

## 🤖 AI Features
- **Smart Categorization**: AI chooses from predefined enum categories
  - Uses transaction description to determine best category
  - Fallback to "MISCELLANEOUS" if uncertain
- **Daily Spending Calculator**: Simple formula for daily budget
  - Formula: `(monthly_income - total_goal_contributions) / days_in_month` - on uses's current money by deadline if going negactive then he has to earn this much money per day to reach his goal...... 
  - Adjust multiplier for preferred spending days
- **Daily Report Generation**: AI-powered daily spending analysis
  - Analyze today's transactions vs budget
  - Identify spending patterns and trends
  - Generate personalized recommendations
  - Compare with previous days/weeks

## 📊 Simple Analytics
- **Daily Reports**: AI-generated daily spending summaries
  - Today's spending vs daily budget
  - Category breakdown for the day
  - Spending patterns and insights
  - Recommendations for tomorrow
- **Monthly Reports**: Basic income vs expense summaries
- **Category Breakdown**: Spending by category charts
- **Goal Progress**: Track progress toward financial goals
- **Daily Budget**: Show remaining daily budget

## 🔔 Receipt OCR (Bonus)
- **Image Upload**: Accept JPG/PNG receipt images
- **OCR Processing**: Extract amount and merchant name
- **Smart Categorization**: AI suggests category based on merchant

## 🚀 API Endpoints
```
Authentication:
POST /auth/google - Google OAuth login
POST /auth/logout - Logout user

Transactions:
GET /transactions - List user transactions (with pagination)
POST /transactions - Create new transaction
PUT /transactions/{id} - Update transaction
DELETE /transactions/{id} - Delete transaction
POST /transactions/upload-receipt - Upload receipt for OCR

Goals:
GET /goals - List user goals
POST /goals - Create new goal
PUT /goals/{id} - Update goal
DELETE /goals/{id} - Delete goal

Analytics:
GET /analytics/daily-report - AI-generated daily spending report
GET /analytics/monthly-report - Monthly income/expense summary
GET /analytics/category-breakdown - Spending by category
GET /analytics/daily-budget - Current daily budget calculation

User:
GET /user/profile - Get user profile
PUT /user/profile - Update user preferences
```

## 🛠️ Tech Stack
- **FastAPI**: Python web framework
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM
- **Google OAuth2**: Authentication
- **Tesseract OCR**: Receipt processing (optional)
- **Pydantic**: Data validation


graph TB
    subgraph "Backend Architecture"
        A[main.py<br/>FastAPI Application] --> B[API Routers]
        B --> C[auth.py<br/>Authentication]
        B --> D[users.py<br/>User Profile]
        B --> E[transactions.py<br/>Transaction CRUD]
        B --> F[goals.py<br/>Goal Management]
        B --> G[analytics.py<br/>Reports & Insights]
        
        H[Models] --> I[base.py<br/>BaseModel]
        H --> J[user.py<br/>User Model]
        H --> K[transaction.py<br/>Transaction Model]
        H --> L[goal.py<br/>Goal Model]
        
        M[Schemas] --> N[auth.py<br/>Auth Schemas]
        M --> O[user.py<br/>User Schemas]
        M --> P[transaction.py<br/>Transaction Schemas]
        M --> Q[goal.py<br/>Goal Schemas]
        
        R[Services] --> S[ai_service.py<br/>Smart Categorization]
        R --> T[budget_calculator.py<br/>Financial Logic]
        
        U[database.py<br/>DB Configuration] --> V[(Database<br/>SQLite/PostgreSQL)]
        
        C --> H
        D --> H
        E --> H
        F --> H
        G --> H
        
        C --> M
        D --> M
        E --> M
        F --> M
        G --> M
        
        G --> R
        E --> R
        
        H --> U
    end
    
    subgraph "Features"
        W[Google OAuth<br/>Authentication]
        X[Smart AI<br/>Categorization]
        Y[Budget<br/>Calculations]
        Z[Analytics &<br/>Reporting]
        AA[Goal<br/>Tracking]
        BB[Transaction<br/>Management]
    end
    
    A --> W
    A --> X
    A --> Y
    A --> Z
    A --> AA
    A --> BB

# SideMoney.ai Backend

Enhanced personal finance tracker backend with AI-powered insights and OCR capabilities.

## 🚀 Features

### Core Features
- **User Authentication** - Google OAuth integration
- **Transaction Management** - Income/expense tracking with smart categorization
- **Goal Setting** - Financial goal tracking with progress monitoring
- **Budget Management** - Daily budget calculations and tracking
- **Analytics & Reporting** - Comprehensive financial analytics

### 🤖 AI-Powered Features
- **Gemini LLM Integration** - Advanced financial analysis and recommendations
- **Smart Categorization** - AI-powered transaction categorization
- **OCR Processing** - Extract transactions from receipts and documents
- **Personalized Insights** - Custom financial advice based on spending patterns
- **Custom AI Queries** - Ask questions about your financial data

## 🔧 Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Google OAuth 2.0
- **AI**: Google Gemini LLM
- **OCR**: Gemini Vision API
- **Validation**: Pydantic v2

## 📦 Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Environment Setup**
Create a `.env` file with:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost/sidemoney

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-flash

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

3. **Run the Application**
```bash
python run.py
```

## 🔗 API Endpoints

### Authentication
- `POST /auth/google` - Google OAuth login
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout

### Transactions
- `GET /transactions` - List transactions (paginated)
- `POST /transactions` - Create transaction
- `GET /transactions/{id}` - Get specific transaction

### Goals
- `GET /goals` - List user goals
- `POST /goals` - Create new goal
- `GET /goals/{id}` - Get specific goal

### Analytics
- `GET /analytics/daily-budget` - Get daily budget info
- `GET /analytics/daily-report` - Get daily spending report

### 🤖 AI Features
- `POST /ai/analyze` - Get comprehensive AI financial analysis
- `POST /ai/ocr/process` - Process receipt/document with OCR
- `POST /ai/query` - Ask custom questions about financial data

### 💳 Transaction Features (with AI)
- `POST /transactions/bulk` - Create bulk transactions from OCR results
- `POST /transactions/categorize` - Get AI transaction categorization

## 🧠 AI Service Features

### 1. Enhanced Financial Analysis
Get structured recommendations and insights powered by Gemini LLM:

```python
# Example API call
POST /ai/analyze?period_days=30

# Response includes:
{
  "recommendations": [
    {
      "title": "Reduce Dining Expenses",
      "description": "You spent $450 on dining this month...",
      "type": "category_reduction",
      "priority": "high",
      "potential_savings": 135.00,
      "action_items": ["Cook 3 meals at home per week", "Set dining budget limit"],
      "category_focus": "FOOD_DINING"
    }
  ],
  "insights": [
    {
      "insight_type": "trend",
      "title": "Increasing Entertainment Spend",
      "description": "Entertainment spending up 25% vs last month",
      "metric_value": 25.0,
      "metric_unit": "percent",
      "trend_direction": "up",
      "severity": "medium"
    }
  ],
  "summary": "Your financial health is good with room for optimization...",
  "confidence_score": 0.87
}
```

### 2. OCR Transaction Extraction
Upload receipts and documents to automatically extract transactions:

```python
# Example usage
POST /ai/ocr/process
Content-Type: multipart/form-data
file: [receipt image]

# Response:
{
  "transactions": [
    {
      "description": "Starbucks Coffee",
      "amount": 5.99,
      "date": "2024-01-15",
      "category": "FOOD_DINING",
      "merchant": "Starbucks",
      "confidence": 0.95
    }
  ],
  "total_amount": 5.99,
  "document_type": "receipt",
  "processing_confidence": 0.88,
  "warnings": []
}
```

### 3. Bulk Transaction Creation
Create multiple transactions from OCR results:

```python
POST /transactions/bulk
{
  "transactions": [
    {
      "description": "Grocery shopping",
      "amount": 45.67,
      "date": "2024-01-15",
      "category": "GROCERIES",
      "confidence": 0.9
    }
  ],
  "source": "ocr",
  "verify_before_save": true
}
```

### 4. Custom AI Queries
Ask personalized questions about your financial data:

```python
POST /ai/query
{
  "user_query": "How can I save more money for my vacation goal?",
  "include_transactions": true,
  "include_goals": true,
  "include_budget": true,
  "period_days": 30
}

# Response includes personalized advice based on actual data
```

## 🎯 Prompt Engineering

The AI service uses sophisticated prompt engineering for:

1. **Financial Analysis Prompts**
   - Structured JSON output format
   - Context-aware recommendations
   - Data-driven insights
   - Actionable advice

2. **OCR Processing Prompts**
   - Multi-format document support
   - Confidence scoring
   - Error handling
   - Structured data extraction

3. **Custom Query Prompts**
   - Context injection
   - User data integration
   - Personalized responses
   - Suggestion extraction

## 🔒 Security

- JWT-based authentication
- User data isolation
- Input validation
- File upload restrictions
- Rate limiting ready

## 📊 Database Models

### Transaction
- User-linked transactions
- Type (income/expense)
- Smart categorization
- Date-based queries

### Goal
- Target amount tracking
- Deadline management
- Progress calculation
- AI-powered recommendations

### User
- Google OAuth profile
- Daily budget settings
- Transaction relationships

## 🚀 Development

### Running Tests
```bash
pytest backend/test_api.py -v
```

### Code Quality
```bash
black backend/
isort backend/
flake8 backend/
```

### Database Migrations
```bash
# Auto-generate migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## 📈 AI Configuration

The AI service automatically falls back to keyword-based categorization if Gemini is unavailable, ensuring robust operation.

### Gemini Models Supported
- `gemini-1.5-flash` (default) - Fast, cost-effective
- `gemini-1.5-pro` - Higher accuracy for complex analysis
- `gemini-1.0-pro-vision` - For OCR processing

### Prompt Engineering Best Practices
- Structured output schemas
- Context-aware prompts
- Fallback mechanisms
- Confidence scoring
- Error handling

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `GEMINI_MODEL` | Gemini model to use | `gemini-1.5-flash` |
| `DATABASE_URL` | PostgreSQL connection | `sqlite:///./sidemoney.db` |
| `SECRET_KEY` | JWT secret key | Development key |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Required |

## 📝 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Include docstrings for public methods
4. Write tests for new features
5. Update documentation

## 📄 License

MIT License - see LICENSE file for details. 

# 🤖 AI Features Setup Guide

## 🚀 Quick Setup

### 1. Environment Configuration

Create a `.env` file in the backend directory with:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/sidemoney
SQL_ECHO=false

# JWT Configuration  
SECRET_KEY=your-super-secret-jwt-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Google OAuth
GOOGLE_CLIENT_ID=your-google-oauth-client-id.apps.googleusercontent.com

# 🤖 Google Generative AI (Gemini) - NEW!
GEMINI_API_KEY=your-gemini-api-key-from-google-ai-studio
GEMINI_MODEL=gemini-1.5-flash

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Production Settings
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1
PORT=8000

# File Upload Settings
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads
```

### 2. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test the Setup

```bash
python test_ai_features.py
```

## 🎯 AI Features Overview

### 1. Enhanced Financial Analysis (`/ai/analyze`)

Get comprehensive AI-powered financial insights with structured recommendations:

**Request:**
```bash
curl -X POST "http://localhost:8000/ai/analyze?period_days=30" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response Structure:**
```json
{
  "recommendations": [
    {
      "title": "Optimize Dining Expenses",
      "description": "You spent $450 on dining this month, which is 30% of your budget...",
      "type": "category_reduction",
      "priority": "high", 
      "potential_savings": 135.00,
      "action_items": [
        "Cook 3 meals at home per week",
        "Set a weekly dining budget of $80",
        "Use meal planning apps"
      ],
      "category_focus": "FOOD_DINING"
    }
  ],
  "insights": [
    {
      "insight_type": "trend",
      "title": "Increasing Entertainment Spend",
      "description": "Entertainment spending increased 25% compared to last month",
      "metric_value": 25.0,
      "metric_unit": "percent",
      "trend_direction": "up",
      "severity": "medium"
    }
  ],
  "summary": "Your financial health is good with room for optimization in dining and entertainment categories.",
  "confidence_score": 0.87
}
```

### 2. OCR Receipt Processing (`/ai/ocr/process`)

Upload receipt images to automatically extract transaction data:

**Request:**
```bash
curl -X POST "http://localhost:8000/ai/ocr/process" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@receipt.jpg"
```

**Response:**
```json
{
  "transactions": [
    {
      "description": "Grande Latte",
      "amount": 5.99,
      "date": "2024-01-15",
      "category": "FOOD_DINING",
      "merchant": "Starbucks",
      "confidence": 0.95
    },
    {
      "description": "Blueberry Muffin", 
      "amount": 3.49,
      "date": "2024-01-15",
      "category": "FOOD_DINING",
      "merchant": "Starbucks",
      "confidence": 0.88
    }
  ],
  "total_amount": 9.48,
  "document_type": "receipt",
  "processing_confidence": 0.91,
  "raw_text": "STARBUCKS\\nGrande Latte $5.99\\nBlueberry Muffin $3.49...",
  "warnings": []
}
```

### 3. Bulk Transaction Creation (`/transactions/bulk`)

Create multiple transactions from OCR results:

**Request:**
```json
{
  "transactions": [
    {
      "description": "Grocery shopping",
      "amount": 45.67,
      "date": "2024-01-15",
      "category": "GROCERIES",
      "confidence": 0.9
    },
    {
      "description": "Gas station fill-up",
      "amount": 52.30,
      "date": "2024-01-15", 
      "category": "TRANSPORTATION",
      "confidence": 0.85
    }
  ],
  "source": "ocr",
  "verify_before_save": false
}
```

**Response:**
```json
{
  "created_count": 2,
  "failed_count": 0,
  "transaction_ids": ["uuid1", "uuid2"],
  "errors": []
}
```

### 4. Custom AI Queries (`/ai/query`)

Ask personalized questions about your financial data:

**Request:**
```json
{
  "user_query": "How can I save $500 more per month for my emergency fund?",
  "include_transactions": true,
  "include_goals": true,
  "include_budget": true,
  "period_days": 30
}
```

**Response:**
```json
{
  "response": "Based on your spending patterns, here are specific ways to save $500 monthly: 1) Reduce dining out from $450 to $200 (save $250), 2) Cancel unused subscriptions (save $50), 3) Use public transport 2 days/week (save $80)...",
  "data_sources": ["Recent transactions", "Financial goals", "Budget information"],
  "suggestions": [
    "Set up automatic transfers to savings",
    "Use the 50/30/20 budgeting rule",
    "Track spending with weekly reviews"
  ],
  "confidence": 0.82
}
```

### 5. Smart Categorization (`/ai/categorize/{description}`)

Get AI-powered transaction categorization:

**Request:**
```bash
curl "http://localhost:8000/ai/categorize/Whole%20Foods%20Market?amount=85.50" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "description": "Whole Foods Market",
  "suggested_category": "GROCERIES",
  "category_display": "Groceries",
  "confidence": "high"
}
```

## 🎯 Prompt Engineering Details

### Financial Analysis Prompts

The AI service uses sophisticated prompts that include:

1. **Structured Output Schema** - Ensures consistent JSON responses
2. **Context Injection** - User's actual financial data
3. **Actionable Guidelines** - Specific instructions for practical advice
4. **Confidence Scoring** - Reliability indicators

**Example Prompt Structure:**
```
You are a professional financial advisor AI. Analyze the user's financial data...

**USER FINANCIAL DATA:**
- Daily Budget: $50.00
- Total Spending: $1,234.56
- [Detailed spending breakdown]

**ANALYSIS REQUIREMENTS:**
1. Provide 3-5 personalized recommendations
2. Include specific action items
3. Calculate potential savings
4. Prioritize by impact

**OUTPUT FORMAT (JSON):** [Structured schema]
```

### OCR Processing Prompts

Advanced prompts for document processing:

1. **Multi-Format Support** - Receipts, statements, invoices
2. **Confidence Scoring** - Per-item and overall confidence
3. **Error Handling** - Graceful degradation
4. **Structured Extraction** - Consistent data format

## 🔧 Advanced Configuration

### Gemini Model Options

```env
# Fast and cost-effective (default)
GEMINI_MODEL=gemini-1.5-flash

# Higher accuracy for complex analysis
GEMINI_MODEL=gemini-1.5-pro

# For vision/OCR tasks
GEMINI_MODEL=gemini-1.0-pro-vision
```

### Fallback Behavior

The AI service includes robust fallback mechanisms:

1. **Gemini Unavailable** → Keyword-based categorization
2. **JSON Parsing Fails** → Text response parsing
3. **OCR Errors** → Basic text extraction
4. **API Limits** → Cached responses

## 🧪 Testing AI Features

### Run Test Suite
```bash
python test_ai_features.py
```

### Manual Testing Examples

1. **Test Categorization:**
```python
from services.ai_service import AIService
category = AIService.categorize_transaction("Starbucks Coffee", 5.99)
print(category)  # ExpenseCategory.FOOD_DINING
```

2. **Test Analysis:**
```python
analysis = AIService.generate_enhanced_analysis(
    user_spending={"FOOD_DINING": 200.0},
    daily_budget=50.0,
    goals=[],
    transactions=[],
    period_days=30
)
```

## 🚨 Production Considerations

### Security
- Store `GEMINI_API_KEY` securely
- Implement rate limiting
- Validate all file uploads
- Monitor API usage

### Performance
- Cache AI responses when appropriate
- Use `gemini-1.5-flash` for speed
- Implement request queuing for high load
- Monitor response times

### Monitoring
- Track AI API usage and costs
- Monitor categorization accuracy
- Log OCR processing results
- Alert on service failures

## 🔍 Troubleshooting

### Common Issues

1. **"Gemini API key not configured"**
   - Set `GEMINI_API_KEY` in `.env`
   - Verify key is valid at Google AI Studio

2. **"OCR processing failed"**
   - Check image file format (JPEG, PNG supported)
   - Verify file size < 10MB
   - Ensure image quality is sufficient

3. **"AI analysis unavailable"**
   - Check internet connection
   - Verify Gemini API quota
   - Review error logs

### Debug Mode

Set environment variables for debugging:
```env
LOG_LEVEL=DEBUG
SQL_ECHO=true
```

## 📈 Future Enhancements

- **Real-time Analysis** - Streaming insights
- **Custom Models** - Fine-tuned categorization
- **Multi-language Support** - International receipts
- **Voice Integration** - Audio transaction entry
- **Predictive Analytics** - Spending forecasts

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Run the test suite for validation
4. Check logs for detailed error information 