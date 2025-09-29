# Ce fichier contient la logique métier (comme un controller)

from sqlalchemy.orm import Session
from .models.count_table import CountTable
from .database import SessionLocal, create_tables

def initialize_count():
    """Initialize the count table with a starting value of 0"""
    db = SessionLocal()
    try:
        # Check if count already exists
        existing_count = db.query(CountTable).first()
        if not existing_count:
            # Create initial count record
            new_count = CountTable(count_number=0)
            db.add(new_count)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error initializing count: {e}")
    finally:
        db.close()

def get_count() -> int:
    """Get the current count value"""
    db = SessionLocal()
    try:
        count_record = db.query(CountTable).first()
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
        db.close()

def increment_count() -> int:
    """Increment the count by 1 and return the new value"""
    db = SessionLocal()
    try:
        count_record = db.query(CountTable).first()
        if count_record:
            count_record.count_number += 1
            db.commit()
            db.refresh(count_record)
            return count_record.count_number
        else:
            # Initialize with 1 if no count exists
            new_count = CountTable(count_number=1)
            db.add(new_count)
            db.commit()
            db.refresh(new_count)
            return new_count.count_number
    except Exception as e:
        db.rollback()
        print(f"Error incrementing count: {e}")
        return get_count()  # Return current count on error
    finally:
        db.close()

def decrement_count() -> int:
    """Decrement the count by 1 and return the new value"""
    db = SessionLocal()
    try:
        count_record = db.query(CountTable).first()
        if count_record:
            count_record.count_number -= 1
            db.commit()
            db.refresh(count_record)
            return count_record.count_number
        else:
            # Initialize with 1 if no count exists
            new_count = CountTable(count_number=1)
            db.add(new_count)
            db.commit()
            db.refresh(new_count)
            return new_count.count_number
    except Exception as e:
        db.rollback()
        print(f"Error incrementing count: {e}")
        return get_count()  # Return current count on error
    finally:
        db.close()

def startup_event():
    """Initialize database and data on startup"""
    create_tables()
    initialize_count()