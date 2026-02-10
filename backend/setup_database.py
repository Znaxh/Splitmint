"""
Database setup script.
Creates all tables using SQLAlchemy models.
"""
from app.models.database import Base
from app.core.database import engine

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
