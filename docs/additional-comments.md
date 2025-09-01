# Additional Comments for Project Submission

**sidemoney.ai - AI-Powered Personal Finance Assistant**

**Key Features Implemented:**

- Complete income/expense transaction management with web interface
- Time-range filtering for transaction listings
- Interactive charts and analytics (expenses by category, date trends, spending patterns)
- Advanced OCR receipt processing for both images and PDF documents
- Multi-user authentication system with Google OAuth
- AI-powered financial insights using Google Gemini
- Pagination support for transaction APIs
- PDF transaction history upload with tabular format support
- Real-time dashboard with financial analytics
- Goal setting and progress tracking
- Responsive design with dark/light theme support

**Technical Stack:**
Frontend: Next.js 14 with TypeScript, Tailwind CSS, shadcn/ui
Backend: FastAPI with Python, PostgreSQL, SQLAlchemy ORM
AI: Google Generative AI (Gemini) for OCR and financial analysis
Authentication: JWT tokens with Google OAuth integration

**How to Run the Application (2 Methods):**

**Method 1 - Docker (Recommended):**

1. Clone the repository
2. Navigate to project directory
3. Run: docker-compose up --build (or docker compose up --build for newer Docker versions)
4. Access frontend at http://localhost:3000
5. Access API docs at http://localhost:8000/docs

**Method 2 - Local Development:**

1. Clone the repository
2. Create PostgreSQL database named 'sidemoney_db'
3. Backend setup:
   - cd backend
   - python -m venv env && source env/bin/activate
   - pip install -r requirements.txt
   - uvicorn main:app --reload --port 8000
4. Frontend setup (new terminal):
   - cd frontend
   - pnpm install && pnpm dev
5. Access application at http://localhost:3000

**Note:** Environment variables are pre-configured in .env files for easy testing. All core requirements and bonus features have been implemented including OCR receipt processing, multi-user support, pagination, and PDF document upload capabilities.
