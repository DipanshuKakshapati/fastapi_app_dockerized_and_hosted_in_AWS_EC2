"""
This module provides a dependency for obtaining a database session.

The get_db function yields a SQLAlchemy database session that is used 
to interact with the database. This function ensures that the session 
is properly closed after use.
"""

from sql_app.database import SessionLocal

def get_db():
    """
    Yields a SQLAlchemy database session.

    This function creates a new SQLAlchemy database session and yields it. 
    After the session is used, it ensures that the session is properly closed.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


