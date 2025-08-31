import os
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

from models import Base

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/sidemoney_db"
)

# For development with SQLite
SQLITE_DATABASE_URL = "sqlite:///./sidemoney.db"

# Use SQLite for development if PostgreSQL URL not provided
if "postgresql://" not in DATABASE_URL and "postgres://" not in DATABASE_URL:
    DATABASE_URL = SQLITE_DATABASE_URL

# SQLAlchemy engine configuration
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"
    )

# Session configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata for migrations
metadata = MetaData()

# Set up logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(
    logging.INFO if os.getenv("SQL_ECHO", "false").lower() == "true" else logging.WARNING
)


def create_database():
    """Create database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise


def drop_database():
    """Drop all database tables"""
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ Database tables dropped successfully")
    except Exception as e:
        print(f"❌ Error dropping database tables: {e}")
        raise


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db_session() -> Session:
    """Get a database session for non-FastAPI usage"""
    return SessionLocal()


class DatabaseManager:
    """Database management utility class"""
    
    @staticmethod
    def check_connection() -> bool:
        """Check if database connection is working"""
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    @staticmethod
    def get_table_count() -> int:
        """Get count of tables in database"""
        try:
            inspector = engine.inspect(engine)
            return len(inspector.get_table_names())
        except Exception:
            return 0
    
    @staticmethod
    def reset_database():
        """Drop and recreate all tables"""
        print("🔄 Resetting database...")
        drop_database()
        create_database()
        print("✅ Database reset complete")
    
    @staticmethod
    def backup_database(backup_path: str = None):
        """Create database backup (PostgreSQL only)"""
        if not backup_path:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_sidemoney_{timestamp}.sql"
        
        if "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL:
            import subprocess
            try:
                subprocess.run([
                    "pg_dump", DATABASE_URL, "-f", backup_path
                ], check=True)
                print(f"✅ Database backup created: {backup_path}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Backup failed: {e}")
        else:
            print("⚠️ Backup only supported for PostgreSQL databases")


# Initialize database on module import for development
if __name__ == "__main__":
    print("🚀 Initializing database...")
    
    # Check connection
    if DatabaseManager.check_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")
        exit(1)
    
    # Create tables if they don't exist
    table_count = DatabaseManager.get_table_count()
    if table_count == 0:
        print("📊 No tables found, creating database schema...")
        create_database()
    else:
        print(f"📊 Found {table_count} existing tables")
    
    print("🎉 Database initialization complete!") 