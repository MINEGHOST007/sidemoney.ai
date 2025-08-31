#!/usr/bin/env python3
"""
SideMoney.ai Backend Server Runner
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    """Run the FastAPI server"""
    print("🚀 Starting SideMoney.ai Backend Server...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    log_level = os.getenv("LOG_LEVEL", "info")
    
    print(f"📡 Server will run on http://{host}:{port}")
    print(f"📚 API docs will be available at http://{host}:{port}/docs")
    print(f"🔄 Reload mode: {'enabled' if reload else 'disabled'}")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        access_log=True
    )


if __name__ == "__main__":
    main() 