from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os
from datetime import datetime

from database import create_database, DatabaseManager
from api import auth_router, users_router, transactions_router, goals_router, analytics_router, ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting SideMoney.ai Backend...")
    
    # Check database connection
    if not DatabaseManager.check_connection():
        print("❌ Database connection failed!")
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Create tables if they don't exist
    try:
        create_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    
    print("🎉 Backend startup complete!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down SideMoney.ai Backend...")


# Create FastAPI application
app = FastAPI(
    title="SideMoney.ai Finance Tracker",
    description="Personal Finance Assistant API for tracking income, expenses, and financial goals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    )

# Include API routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(transactions_router)
app.include_router(goals_router)
app.include_router(analytics_router)
app.include_router(ai_router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to SideMoney.ai Finance Tracker API",
        "description": "Clean, modular backend with separated APIs for better readability",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "features": [
            "Google OAuth Authentication",
            "Smart AI Categorization", 
            "Budget Calculations with Current Amount",
            "Goal Progress Tracking",
            "Analytics & Reporting",
            "Paginated Transaction Management",
            "AI-Powered Insights"
        ],
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_healthy = DatabaseManager.check_connection()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": str(datetime.now())
    }


if __name__ == "__main__":
    import uvicorn
    
    # Development server configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    ) 