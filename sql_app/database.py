"""
This module sets up the SQLAlchemy connection to a Microsoft SQL Database using ODBC.

It configures environment variables required for the ODBC driver, establishes the connection
string to the database, and initializes SQLAlchemy components including the engine, session,
and base class for declarative models.

Environment variables set:
    - ODBCINI: Path to the ODBC initialization file.
    - ODBCSYSINI: Path to the ODBC system configuration directory.
    - DYLD_LIBRARY_PATH: Path to the dynamic linker library.

Connection string:
    - DATABASE_URL: Connection string for the Microsoft SQL Database with ODBC Driver 17.

SQLAlchemy components:
    - engine: The SQLAlchemy engine bound to the database.
    - SessionLocal: A configured sessionmaker for creating new sessions.
    - Base: A declarative base class for defining ORM models.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')
#DATABASE_URL = "postgresql+psycopg2://postgres:Ocacine10#@localhost:5432/fastapi"
engine = create_engine(DATABASE_URL)

# Try connecting
with engine.connect() as conn:
    result = conn.execute("SELECT version();")  # Corrected SQL command to get PostgreSQL server version
    print(result.fetchone())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()






