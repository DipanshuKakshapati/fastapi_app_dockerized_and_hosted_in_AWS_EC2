"""
This module defines the Pydantic models for data validation of the 'nepse' table entries.
These models are utilized to validate incoming data for the API, ensuring that it adheres
to the expected structure and data types before it is processed by the application.
"""

from datetime import date
from pydantic import BaseModel

class NepseBase(BaseModel):
    """
    A base model representing the 'nepse' table schema, used for data validation.
    """

    Sn:int
    Symbol:str
    Close_Price_Rs:float
    Open_Price_Rs:float
    High_Price_Rs: float
    Low_Price_Rs: float
    Total_Traded_Quantity: int
    Total_Traded_Value: float
    Total_Trades: int
    LTP: str
    Previous_Day_Close_Price_Rs: float
    Average_Traded_Price_Rs: float
    Fifty_Two_Week_High_Rs: float
    Fifty_Two_Week_Low_Rs: float
    Market_Capitalization_Rs__Amt_in_Millions: float
    Close_Date: date

    class Config:
        """
        Configuration settings for the Pydantic model, enabling compatibility with ORM models and other settings.
        """
        orm_mode = True
    
    

