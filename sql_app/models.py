"""
This module defines the database schema for the 'nepse' table using SQLAlchemy's ORM.

It includes the Nepse class which maps to the 'nepse' table in the database. This class
provides a structured model to interact with the Nepse stock market transaction data, 
facilitating easy reading and writing to the database using SQLAlchemy session operations.

The schema includes various financial metrics such as close price, high price, and 
other stock-related data for a given date.

Example:
    To use this model within a SQLAlchemy session context:
    
    from database.session import SessionLocal
    from models.nepse import Nepse
    
    db_session = SessionLocal()
    nepse_data = db_session.query(Nepse).filter(Nepse.Closed_Date == '2021-01-01').first()
    print(nepse_data.Close)  # Accessing the close price

"""

import sqlalchemy as sa
from sql_app.database import Base

# defining 'nepse' table model
class Nepse(Base):
    """
    Represents a record in the 'nepse' table, containing details of stock market transactions.

    Attributes:
        Sn (int): Serial number, primary key, not nullable.
        Symbol (str): Stock symbol.
        Close_Price_Rs (float): Closing price of the stock on the given date.
        Open_Price_Rs (float): Opening price of the stock on the given date.
        High_Price_Rs (float): Highest price of the stock on the given date.
        Low_Price_Rs (float): Lowest price of the stock on the given date.
        Total_Traded_Quantity (int): Total traded quantity of the stock on the given date.
        Total_Traded_Value (float): Total traded value of the stock on the given date.
        Total_Trades (int): Total number of trades made on the given date.
        LTP (str): Last traded price.
        Previous_Day_Close_Price_Rs (float): Closing price of the stock on the previous day.
        Average_Traded_Price_Rs (float): Average traded price of the stock on the given date.
        Fifty_Two_Week_High_Rs (float): Highest price of the stock in the last 52 weeks.
        Fifty_Two_Week_Low_Rs (float): Lowest price of the stock in the last 52 weeks.
        Market_Capitalization_Rs__Amt_in_Millions (float): Market capitalization in millions of rupees.
        Close_Date (date): The date of the transaction.
    """
    __tablename__ = 'nepse'

    Sn = sa.Column(sa.Integer, primary_key=True, nullable=False)
    Symbol = sa.Column(sa.String)
    Close_Price_Rs = sa.Column(sa.Float)
    Open_Price_Rs = sa.Column(sa.Float)
    High_Price_Rs = sa.Column(sa.Float)
    Low_Price_Rs = sa.Column(sa.Float)
    Total_Traded_Quantity = sa.Column(sa.Integer)
    Total_Traded_Value = sa.Column(sa.Float)
    Total_Trades = sa.Column(sa.Integer)
    LTP = sa.Column(sa.String)
    Previous_Day_Close_Price_Rs = sa.Column(sa.Float)
    Average_Traded_Price_Rs = sa.Column(sa.Float)
    Fifty_Two_Week_High_Rs = sa.Column(sa.Float)
    Fifty_Two_Week_Low_Rs = sa.Column(sa.Float)
    Market_Capitalization_Rs__Amt_in_Millions = sa.Column(sa.Float)
    Close_Date = sa.Column(sa.Date)


