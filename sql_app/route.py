"""
This module defines the FastAPI routes for retrieving environment variables and 
stock market data from the Microsoft SQL database. It includes endpoints for fetching environment 
configuration details and stock market data for a specific date. The module utilizes 
SQLAlchemy for database interactions and FastAPI for request handling.

Endpoints:
    - /env: Returns environment variables related to ODBC configuration.
    - /stocks_data: Crete a stock record, Read stock data from a specific symbol and close date, Update a stock record, and Delete a stock data from a specific symbol and date
"""
import os
import time
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sql_app.session import get_db
from sql_app.functions import convert_date_format, process_html_to_dataframe_date, process_html_to_dataframe_symbol
from sql_app.models import Nepse

router = APIRouter()

@router.get("/env")
def read_env():
    """
    Get and return environment variables related to ODBC configuration.

    This endpoint returns the values of the 'ODBCINI', 'ODBCSYSINI', and 
    'DYLD_LIBRARY_PATH' environment variables. These variables are important 
    for configuring ODBC connections in the application.

    Returns:
        dict: A dictionary containing the values of the specified environment variables.
    """
    return {
        "ODBCINI": os.getenv("ODBCINI"),
        "ODBCSYSINI": os.getenv("ODBCSYSINI"),
        "DYLD_LIBRARY_PATH": os.getenv("DYLD_LIBRARY_PATH"),
    }

# creating a stock data
@router.post("/stocks_data")
async def add_stock(symbol: str, 
                    close_price_rs: float, 
                    open_price_rs: float, 
                    high_price_rs: float, 
                    low_price_rs: float, 
                    total_traded_quantity: int, 
                    total_traded_value: float, 
                    total_trades: int, 
                    ltp: str, 
                    previous_day_close_price_rs: float, 
                    average_traded_price_rs: float, 
                    fifty_two_week_high_rs: float, 
                    fifty_two_week_low_rs: float, 
                    market_capitalization_rs__amt_in_millions: float, 
                    close_date: str, db: Session = Depends(get_db)):
    """
    Add a new stock entry to the database.
    
    Returns:
    - Nepse: The created Nepse stock record.
    """

     # converting close_date from string to datetime object to ensure correct formatting
    try:
        parsed_close_date = datetime.strptime(close_date, "%Y-%m-%d")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD format.") from ve

    data = Nepse(
        Symbol=symbol,
        Close_Price_Rs=close_price_rs,
        Open_Price_Rs=open_price_rs,
        High_Price_Rs=high_price_rs,
        Low_Price_Rs=low_price_rs,
        Total_Traded_Quantity=total_traded_quantity,
        Total_Traded_Value=total_traded_value,
        Total_Trades=total_trades,
        LTP=ltp,
        Previous_Day_Close_Price_Rs=previous_day_close_price_rs,
        Average_Traded_Price_Rs=average_traded_price_rs,
        Fifty_Two_Week_High_Rs=fifty_two_week_high_rs,
        Fifty_Two_Week_Low_Rs=fifty_two_week_low_rs,
        Market_Capitalization_Rs__Amt_in_Millions=market_capitalization_rs__amt_in_millions,
        Close_Date=parsed_close_date
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# updating a stock data by specifing it's symbol and close date
@router.put("/stocks_data")
async def update_stock(symbol: str, 
                       close_price_rs: float, 
                       open_price_rs: float, 
                       high_price_rs: float, 
                       low_price_rs: float, 
                       total_traded_quantity: int, 
                       total_traded_value: float, 
                       total_trades: int, 
                       ltp: str, 
                       previous_day_close_price_rs: float, 
                       average_traded_price_rs: float, 
                       fifty_two_week_high_rs: float, 
                       fifty_two_week_low_rs: float, 
                       market_capitalization_rs_amt_in_millions: float, 
                       close_date: str, db: Session = Depends(get_db)):
    """
    Update a stock record for a given symbol and close date.
    """
    try:
        # converting close_date from string to datetime object to ensure correct formatting
        parsed_close_date = datetime.strptime(close_date, "%Y-%m-%d")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD format.") from ve

    # getting the first matching stock record
    item = db.query(Nepse).filter(and_(Nepse.Close_Date == parsed_close_date, Nepse.Symbol == symbol)).first()

    if not item:
        raise HTTPException(status_code=404, detail="Stock record not found.")

    # updating the fields of the stock record
    item.Close_Price_Rs = close_price_rs
    item.Open_Price_Rs = open_price_rs
    item.High_Price_Rs = high_price_rs
    item.Low_Price_Rs = low_price_rs
    item.Total_Traded_Quantity = total_traded_quantity
    item.Total_Traded_Value = total_traded_value
    item.Total_Trades = total_trades
    item.LTP = ltp
    item.Previous_Day_Close_Price_Rs = previous_day_close_price_rs
    item.Average_Traded_Price_Rs = average_traded_price_rs
    item.Fifty_Two_Week_High_Rs = fifty_two_week_high_rs
    item.Fifty_Two_Week_Low_Rs = fifty_two_week_low_rs
    item.Market_Capitalization_Rs_Amt_in_Millions = market_capitalization_rs_amt_in_millions
    item.Close_Date = parsed_close_date

    db.commit()
    db.refresh(item)
    return item

# webscrap query parameter to get stock data by date
@router.get("/stocks_data_date")
async def get_stock_by_date(
    date: str = Query(None, description="Enter the date in YYYY-MM-DD format"), 
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="Page number, starting from 1"),
    page_size: int = Query(5, gt=0, le=100, description="Number of records per page, max 100")
):
    
    """
    Retrieve stock market data filtered by a specific date from the database. If no data is available in the database,
    attempt to scrape the required data from a specified website.

    Args:
        date (str): Date for which the stock data is requested, in the format YYYY-MM-DD.
        db (Session): Database session dependency that provides a session for querying the database.
        page (int): The page number of the results to return.
        page_size (int): The number of records to return per page.

    Raises:
        HTTPException: If the date format is incorrect or database operations fail.

    Returns:
        dict: A dictionary containing paginated stock data and metadata about pagination.
    """

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid date format, please use YYYY-MM-DD format.") from ve

    try:
        offset = (page - 1) * page_size
        data = (db.query(Nepse)
                  .filter(Nepse.Close_Date == date_obj)
                  .order_by(Nepse.Sn)  # ensuring consistent ordering for pagination
                  .offset(offset)
                  .limit(page_size)
                  .all())
    except SQLAlchemyError as db_err:
        raise HTTPException(status_code=500, detail=str(db_err)) from db_err

    if data:

        # transforming data into a dictionary format suitable for JSON response
        data_dict = [{
            "Sn": item.Sn, 
            "Symbol": item.Symbol, 
            "Close_Price_Rs": item.Close_Price_Rs, 
            "Open_Price_Rs": item.Open_Price_Rs,
            "High_Price_Rs": item.High_Price_Rs, 
            "Low_Price_Rs": item.Low_Price_Rs,
            "Total_Traded_Quantity": item.Total_Traded_Quantity,
            "Total_Traded_Value": item.Total_Traded_Value,
            "Total_Trades": item.Total_Trades,
            "LTP": item.LTP,
            "Previous_Day_Close_Price_Rs": item.Previous_Day_Close_Price_Rs,
            "Average_Traded_Price_Rs": item.Average_Traded_Price_Rs,
            "Fifty_Two_Week_High_Rs": item.Fifty_Two_Week_High_Rs,
            "Fifty_Two_Week_Low_Rs": item.Fifty_Two_Week_Low_Rs,
            "Market_Capitalization_Rs__Amt_in_Millions": item.Market_Capitalization_Rs__Amt_in_Millions,
            "Close_Date": item.Close_Date
        } for item in data]

        return {"data": data_dict, "page": page, "page_size": page_size, "total_records": db.query(Nepse).filter(Nepse.Close_Date == date_obj).count()}

    if not data:
        try:
            formatted_date = convert_date_format(date)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail="Date format should be YYYY-MM-DD") from ve

        # setting up Firefox in headless mode
        options = FirefoxOptions()
        options.add_argument("--headless")

        # setting the path to geckodriver using Service
        service = FirefoxService(executable_path=r"/usr/local/bin/geckodriver")

        driver = webdriver.Firefox(service=service, options=options)

        try:
            driver.get("https://nepalstock.com/today-price")
            time.sleep(2)
            select = Select(driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[3]/select'))
            select.select_by_visible_text('500')
            time.sleep(2)
            
            input_field = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[1]/div/input')
            input_field.clear()
            input_field.send_keys(formatted_date) 
            input_field.send_keys(Keys.ENTER)
            time.sleep(2)

            filter_button = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[4]/button[1]')
            filter_button.click()
            time.sleep(2)

            table_element = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[3]')
            inner_html = table_element.get_attribute('innerHTML')
        finally:
            driver.quit()

        data_frame = process_html_to_dataframe_date(inner_html, date)
        
        if data_frame.empty:
            return {"message": "No data found for the specified date"}
        
        # pagination logic for the DataFrame
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_data = data_frame.iloc[start_index:end_index]

        if paginated_data.empty:
            return {"message": "No data found on this page"}

        return {
            "data": paginated_data.to_dict(orient='records'),
            "page": page,
            "page_size": page_size,
            "total_records": len(data_frame)
        }

# webscrap query parameter to get stock data by date and symbol
@router.get("/stocks_data_date_and_symbol")
async def get_stock_by_date_and_symbol(
    date: str = Query(None, description="Enter the date in YYYY-MM-DD format"), 
    symbol: str = Query(None, description="Enter the stock symbol"),
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="Page number, starting from 1"),
    page_size: int = Query(5, gt=0, le=100, description="Number of records per page, max 100")
):
    
    """
    Retrieve or scrape stock market data for a specific symbol on a given date. This function first tries to fetch the
    data from a database. If not available, it attempts to scrape the data from a web page.

    Args:
        date (str): The date for which stock data is requested, in the format YYYY-MM-DD.
        symbol (str): The stock symbol for which data is being queried.
        db (Session): Database session dependency injected by FastAPI to handle database operations.
        page (int): The page number for pagination of results.
        page_size (int): The number of results to return per page, with a maximum of 100 records per page.

    Raises:
        HTTPException: Raised if the date format is incorrect, if the database operations fail, or if web scraping
                        fails due to changes on the target website.

    Returns:
        dict: A dictionary containing the paginated stock data and metadata such as page number, page size,
              and total records found. If no data is found, returns a message indicating no data was found.
    """
        
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid date format, please use YYYY-MM-DD format.") from ve

    try:
        offset = (page - 1) * page_size
        data = (db.query(Nepse)
                  .filter(and_(Nepse.Close_Date == date_obj))
                  .order_by(Nepse.Sn)  # ensuring consistent ordering for pagination
                  .offset(offset)
                  .limit(page_size)
                  .first())
    except SQLAlchemyError as db_err:
        raise HTTPException(status_code=500, detail="Database operation failed") from db_err

    if data:
        # transforming data into a dictionary format suitable for JSON response
        data_dict = [{
            "Sn": item.Sn, 
            "Symbol": item.Symbol, 
            "Close_Price_Rs": item.Close_Price_Rs, 
            "Open_Price_Rs": item.Open_Price_Rs,
            "High_Price_Rs": item.High_Price_Rs, 
            "Low_Price_Rs": item.Low_Price_Rs,
            "Total_Traded_Quantity": item.Total_Traded_Quantity,
            "Total_Traded_Value": item.Total_Traded_Value,
            "Total_Trades": item.Total_Trades,
            "LTP": item.LTP,
            "Previous_Day_Close_Price_Rs": item.Previous_Day_Close_Price_Rs,
            "Average_Traded_Price_Rs": item.Average_Traded_Price_Rs,
            "Fifty_Two_Week_High_Rs": item.Fifty_Two_Week_High_Rs,
            "Fifty_Two_Week_Low_Rs": item.Fifty_Two_Week_Low_Rs,
            "Market_Capitalization_Rs__Amt_in_Millions": item.Market_Capitalization_Rs__Amt_in_Millions,
            "Close_Date": item.Close_Date
        } for item in data]

        return {"data": data_dict, "page": page, "page_size": page_size, "total_records": db.query(Nepse).filter(Nepse.Close_Date == date_obj).count()}

    if not data:
        try:
            formatted_date = convert_date_format(date)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail="Date format should be YYYY-MM-DD") from ve

        # setting up Firefox in headless mode
        options = FirefoxOptions()
        options.add_argument("--headless")

        # making sure to provide the full path to the 'geckodriver' in your system
        # setting the path to geckodriver using Service
        service = FirefoxService(executable_path=r"/usr/local/bin/geckodriver")

        driver = webdriver.Firefox(service=service, options=options)

        try:
            driver.get("https://nepalstock.com/today-price")
            time.sleep(2)
            input_field = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[1]/div/input')
            input_field.clear()
            input_field.send_keys(formatted_date)  # using the converted date
            input_field.send_keys(Keys.ENTER)
            time.sleep(2)
                        
            input_field_text = driver.find_element(by=By.XPATH, value='/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[2]/input')

            # clearing the input field before sending new date text
            input_field_text.clear()

            input_field_text.send_keys(symbol)

            input_field_text.send_keys(Keys.ENTER)

            time.sleep(2)

            filter_button = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[4]/button[1]')
            filter_button.click()
            time.sleep(2)

            table_element = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[3]')
            inner_html = table_element.get_attribute('innerHTML')
            
        finally:
            driver.quit()

        data_frame = process_html_to_dataframe_symbol(inner_html, date)
        
        if data_frame.empty:
            return {"message": "No data found for the specified date"}
        
        # pagination logic for the DataFrame
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_data = data_frame.iloc[start_index:end_index]

        if paginated_data.empty:
            return {"message": "No data found on this page"}

        return {
            "data": paginated_data.to_dict(orient='records'),
            "page": page,
            "page_size": page_size,
            "total_records": len(data_frame)
        }
    
# deleting a stock data by symbol and close date
@router.delete("/stocks_data")
async def delete_stock_by_symbol_and_date(symbol: str, 
                                          close_date: str, 
                                          db: Session = Depends(get_db)):
    """
    Delete stock data for a specific symbol on a given date.
    
    Parameters:
    - symbol (str): The stock symbol.
    - close_date (str): The date for which stock data should be deleted (YYYY-MM-DD).
    - db (Session, optional): Database session dependency.
    
    Raises:
    - HTTPException: If the close_date is in the wrong format or no stock is found.
    
    Returns:
    - dict: Confirmation message of deletion.
    """
    try:
        # converting close_date from string to datetime object to ensure correct formatting
        parsed_close_date = datetime.strptime(close_date, "%Y-%m-%d")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD format.") from ve
    
    # getting the stock data to be deleted
    data_to_delete = db.query(Nepse).filter(and_(Nepse.Symbol == symbol, Nepse.Close_Date == parsed_close_date)).all()

    if not data_to_delete:
        raise HTTPException(status_code=404, detail="No stock found with the given symbol and date.")
    
    # iterating over found stock data and deleting them
    for item in data_to_delete:
        db.delete(item)
        
    db.commit()
    return {"message": f"Stock {symbol} from the date {close_date} deleted successfully!"}