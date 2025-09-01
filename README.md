<div align="center">
  
# 💰 SideMoney.ai

**AI-Powered Personal Finance Assistant**

_Spend smarter. Save faster._

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.16-000000.svg)](https://nextjs.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com)

[🚀 Live Demo](#) • [📖 Documentation](#) • [🐛 Report Bug](#) • [💡 Request Feature](#)

</div>

---

## 🎬 Demo Video

<!-- Placeholder for main demo video -->

[![SideMoney.ai Demo](https://img.shields.io/badge/▶️-Watch%20Demo-red.svg?style=for-the-badge)](YOUR_DEMO_VIDEO_URL)

_Insert your demo video here showing the key features of the application_

---

## 📱 Screenshots

### 🏠 Landing Page

<!-- Placeholder for landing page screenshot -->

![Landing Page](./docs/screenshots/landing-page.png)
_Clean, modern landing page with feature highlights_

### 📊 Dashboard Overview

<!-- Placeholder for dashboard screenshot -->

![Dashboard](./docs/screenshots/dashboard.png)
_Real-time financial insights and analytics at a glance_

### 🤖 AI-Powered OCR Receipt & Document Upload

<!-- Placeholder for OCR feature screenshot -->

![OCR Upload](./docs/screenshots/ocr-upload.png)
_Upload receipts, invoices, and PDF documents - AI extracts transaction details automatically_

**NEW: PDF Support Added!** 📄

- Upload PDF receipts, bank statements, and invoices
- Intelligent text extraction from digital PDFs
- Automatic conversion of scanned PDFs to images for OCR
- Multi-page document processing (first 3 pages)

### 📈 Analytics & Reports

<!-- Placeholder for analytics screenshot -->

![Analytics](./docs/screenshots/analytics.png)
_Comprehensive spending analysis and trend visualization_

### 🎯 Goals Tracking

<!-- Placeholder for goals screenshot -->

![Goals](./docs/screenshots/goals.png)
_Set and track your financial goals with progress monitoring_

---

## ✨ Features

### 🧠 **AI-Powered Intelligence**

- **Smart OCR Receipt & Document Processing**: Upload images AND PDF documents - AI extracts transaction details
- **PDF Document Support**: Process bank statements, invoices, and receipts in PDF format
- **AI Daily Spending Reports**: Get personalized insights powered by Google Gemini
- **Intelligent Transaction Categorization**: Automatic expense categorization with AI
- **Financial Recommendations**: AI-driven suggestions for better money management

### 💳 **Transaction Management**

- **Real-time Transaction Tracking**: Add, edit, and categorize transactions instantly
- **Multiple Transaction Types**: Support for income, expenses, and transfers
- **Advanced Filtering**: Filter by date range, category, amount, and transaction type
- **Bulk Import**: Process multiple transactions from OCR or manual entry

### 📊 **Analytics & Insights**

- **Interactive Charts**: Beautiful visualizations of spending patterns
- **Spending Trends**: Track your financial habits over time
- **Category Breakdown**: Detailed analysis of spending by category
- **Budget Monitoring**: Stay on track with your financial goals

### 🎯 **Goals & Planning**

- **Smart Goal Setting**: Create and track financial objectives
- **Progress Monitoring**: Visual progress tracking for each goal
- **Goal Recommendations**: AI-suggested goals based on your spending patterns
- **Achievement Milestones**: Celebrate your financial wins

### 🔐 **Security & Authentication**

- **Google OAuth Integration**: Secure sign-in with Google authentication
- **JWT Token Security**: Industry-standard authentication tokens
- **Data Privacy**: Your financial data is encrypted and secure

### 🎨 **Modern UI/UX**

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark/Light Theme**: Choose your preferred visual experience
- **Intuitive Interface**: Clean, user-friendly design
- **Real-time Updates**: Live data synchronization across all features

---

## 🛠️ Tech Stack

### **Frontend**

- **Framework**: Next.js 14.2.16 with TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **UI Components**: Radix UI primitives
- **Icons**: Lucide React
- **Charts**: Recharts for data visualization
- **Forms**: React Hook Form with Zod validation

### **Backend**

- **Framework**: FastAPI 0.104.1 (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with Google OAuth
- **AI Integration**: Google Generative AI (Gemini)
- **Document Processing**: Pillow, PyPDF2, pdf2image for OCR & PDF support
- **API Documentation**: Automatic OpenAPI/Swagger docs

### **Infrastructure**

- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15
- **Web Server**: Uvicorn with Gunicorn
- **Environment Management**: Python virtual environment

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 18+
- pnpm (recommended) or npm

### 🐳 Docker Setup (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/MINEGHOST007/sidemoney.ai.git
   cd sidemoney.ai
   ```

2. **Set up environment variables**

   ```bash
   # Backend environment
   cp backend/.env.example backend/.env

   # Frontend environment
   cp frontend/.env.example frontend/.env
   ```

3. **Configure your environment files**

   ```env
   # backend/.env
   DATABASE_URL=postgresql://postgres:postgres@db:5432/sidemoney_db
   SECRET_KEY=your_jwt_secret_key_here
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GEMINI_API_KEY=your_gemini_api_key

   # frontend/.env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id
   ```

4. **Start the application**

   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### 🛠️ Development Setup

#### Backend Setup

```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend
pnpm install
pnpm dev
```

---

## 📝 API Documentation

The API is fully documented with OpenAPI/Swagger. Once the backend is running, visit:

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### 🔐 Authentication

- `POST /auth/google` - Google OAuth login
- `GET /auth/me` - Get current user info

#### 💳 Transactions

- `GET /transactions` - List transactions with filtering
- `POST /transactions` - Create new transaction
- `POST /transactions/bulk` - Bulk create from OCR

#### 🧠 AI Features

- `POST /ai/analyze` - Get AI financial analysis
- `POST /ai/ocr` - Process receipt image with OCR
- `POST /ai/chat` - Chat with AI assistant

#### 🎯 Goals

- `GET /goals` - List user goals
- `POST /goals` - Create new goal
- `PUT /goals/{id}` - Update goal progress

#### 📊 Analytics

- `GET /analytics/spending` - Spending analytics
- `GET /analytics/trends` - Financial trends
- `GET /analytics/categories` - Category breakdown

---

## 🎯 Usage Examples

### OCR Receipt Processing

<!-- Placeholder for OCR workflow GIF -->

![OCR Workflow](./docs/gifs/ocr-workflow.gif)
_Upload a receipt image and watch AI extract transaction details_

```python
# Example OCR API usage
curl -X POST "http://localhost:8000/ai/ocr" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@receipt.jpg"
```

### AI Financial Analysis

<!-- Placeholder for AI analysis GIF -->

![AI Analysis](./docs/gifs/ai-analysis.gif)
_Get personalized financial insights and recommendations_

```python
# Get 30-day financial analysis
curl -X POST "http://localhost:8000/ai/analyze?period_days=30" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
pnpm test
```

---

## 📂 Project Structure

```
sidemoney.ai/
├── 🗂️ backend/
│   ├── 📁 api/           # FastAPI route handlers
│   ├── 📁 models/        # SQLAlchemy database models
│   ├── 📁 schemas/       # Pydantic schemas
│   ├── 📁 services/      # Business logic services
│   ├── 📁 tests/         # Backend tests
│   └── 📄 main.py        # FastAPI application entry
├── 🗂️ frontend/
│   ├── 📁 app/           # Next.js App Router
│   ├── 📁 components/    # React components
│   ├── 📁 lib/           # Utility functions
│   ├── 📁 hooks/         # Custom React hooks
│   └── 📁 styles/        # Global styles
├── 🗂️ docs/
│   ├── 📁 screenshots/   # Application screenshots
│   └── 📁 gifs/          # Demo animations
├── 🐳 docker-compose.yml
└── 📄 README.md
```

---

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Write tests for new features
- Update documentation as needed

---

## 🎯 Roadmap

### 🚧 Coming Soon

- [ ] **Mobile App**: React Native mobile application
- [ ] **Bank Integration**: Connect with bank APIs for automatic transaction import
- [ ] **Investment Tracking**: Portfolio management and investment insights
- [ ] **Bill Reminders**: Smart notifications for upcoming bills
- [ ] **Expense Splitting**: Share expenses with friends and family
- [ ] **Advanced Budgeting**: More sophisticated budgeting tools
- [ ] **Multi-Currency Support**: International currency handling
- [ ] **Export Features**: PDF reports and data export options

### 🔮 Future Enhancements

- [ ] **Machine Learning Models**: Custom ML models for better predictions
- [ ] **Voice Commands**: Voice-activated transaction entry
- [ ] **Cryptocurrency Tracking**: Digital asset management
- [ ] **Tax Preparation**: Automated tax document generation
- [ ] **Financial Planning**: Long-term financial planning tools

---

## 🐛 Known Issues

- OCR accuracy may vary with image quality
- Large transaction datasets may have slower load times
- Mobile responsiveness is optimized for modern devices

---

## 📞 Support

- **Documentation**: Check our [Wiki](#) for detailed guides
- **Issues**: Report bugs in our [Issue Tracker](#)
- **Discussions**: Join our [Community Discussions](#)
- **Email**: support@sidemoney.ai

---

## Acknowledgments

- **Google Generative AI** for powering our AI features
- **OpenAI** for inspiration and AI development patterns
- **Vercel** for excellent Next.js documentation
- **FastAPI** community for the amazing framework
- **shadcn/ui** for beautiful UI components

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/MINEGHOST007/sidemoney.ai?style=social)
![GitHub forks](https://img.shields.io/github/forks/MINEGHOST007/sidemoney.ai?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/MINEGHOST007/sidemoney.ai?style=social)

---

<div align="center">

**Built with ❤️ by [MINEGHOST007](https://github.com/MINEGHOST007)**

_If you found this project helpful, please consider giving it a ⭐!_

</div>
