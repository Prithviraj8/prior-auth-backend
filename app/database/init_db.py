from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from .session import engine
from ..models.base_models import AuthRequest, User

def init_db():
    # Import all models that should create tables
    from ..models.base_models import AuthRequest, User
    
    # Create all tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!") 