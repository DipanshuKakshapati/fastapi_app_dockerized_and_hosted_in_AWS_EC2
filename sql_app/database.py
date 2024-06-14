"""
This module sets up a connection to a MySQL database using SQLAlchemy and performs a basic database operation.
It uses environment variables for configuration to enhance security and modularity.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

username = os.environ.get('username')
password = os.environ.get('password')
database = os.environ.get('database')
server = os.environ.get('server')
port = int(os.environ.get('port'))

DATABASE_URL = "mysql+pymysql://{username}:{password}@{server}:{port}/{database}"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute("SELECT VERSION()")
    print(result.fetchone())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
