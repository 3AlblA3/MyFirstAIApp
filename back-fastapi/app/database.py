# Ce fichier a été modifié pour séparer les responsabilités
# et éviter de mélanger la définition du modèle avec la configuration de la base de données

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@postgres:5432/mydb")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)