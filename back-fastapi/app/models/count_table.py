import os
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CountTable(Base):
    __tablename__ = 'count_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    count_number = Column(Integer, nullable=False)

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@postgres:5432/mydb")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)

def initialize_count():
    """Initialize the count table with a starting value of 0"""
    session = Session()
    try:
        # Check if count already exists
        existing_count = session.query(CountTable).first()
        if not existing_count:
            # Create initial count record
            new_count = CountTable(count_number=0)
            session.add(new_count)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error initializing count: {e}")
    finally:
        session.close()

def get_count():
    """Get the current count value"""
    session = Session()
    try:
        count_record = session.query(CountTable).first()
        if count_record:
            return count_record.count_number
        else:
            # Initialize if no count exists
            initialize_count()
            return 0
    except Exception as e:
        print(f"Error getting count: {e}")
        return 0
    finally:
        session.close()

def increment_count():
    """Increment the count by 1 and return the new value"""
    session = Session()
    try:
        count_record = session.query(CountTable).first()
        if count_record:
            count_record.count_number += 1
            session.commit()
            return count_record.count_number
        else:
            # Initialize with 1 if no count exists
            new_count = CountTable(count_number=1)
            session.add(new_count)
            session.commit()
            return 1
    except Exception as e:
        session.rollback()
        print(f"Error incrementing count: {e}")
        return get_count()  # Return current count on error
    finally:
        session.close()

# Initialize count on module import
initialize_count()