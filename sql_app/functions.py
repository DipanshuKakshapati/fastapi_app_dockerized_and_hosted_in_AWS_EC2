"""
This module provides functions to convert date formats, process HTML content into pandas DataFrames, and safely convert
strings to float or integer types. These functions are primarily used for extracting and manipulating stock data obtained
from web scraping.
"""

from datetime import datetime
import pandas as pd
from lxml import html

def convert_date_format(iso_date_str):

    """Converts date from 'YYYY-MM-DD' to 'MM/DD/YYYY'."""
    
    date_obj = datetime.strptime(iso_date_str, "%Y-%m-%d")
    return date_obj.strftime("%m/%d/%Y")

def process_html_to_dataframe_date(html_content, date_str):

    """Processes HTML content to extract stock data and return as a DataFrame."""

    root = html.fromstring(html_content)
    data = {
        'Symbol': [],
        'Close_Price_Rs': [],
        'Open_Price_Rs': [],
        'High_Price_Rs': [],
        'Low_Price_Rs': [],
        'Total_Traded_Quantity': [],
        'Total_Traded_Value': [],
        'Total_Trades': [],
        'LTP': [],
        'Previous_Day_Close_Price_Rs': [],
        'Average_Traded_Price_Rs': [],
        'Fifty_Two_Week_High_Rs': [],
        'Fifty_Two_Week_Low_Rs': [],
        'Market_Capitalization_Rs__Amt_in_Millions': [],
        'Close_Date': []
    }
        # processing each row in the table
    for row in root.xpath('//tr[position() > 1]'):
        # ensuring each data list gets a value even if cells are missing
        cells = [cell.text_content().strip() for cell in row.xpath('.//td')]
        if len(cells) != 15:
            continue

        # appending data to each key in the dictionary, converting types as needed
        data['Symbol'].append(cells[1])
        data['Close_Price_Rs'].append(safe_float(cells[2]))
        data['Open_Price_Rs'].append(safe_float(cells[3]))
        data['High_Price_Rs'].append(safe_float(cells[4]))
        data['Low_Price_Rs'].append(safe_float(cells[5]))
        data['Total_Traded_Quantity'].append(safe_int(cells[6]))
        data['Total_Traded_Value'].append(safe_float(cells[7]))
        data['Total_Trades'].append(safe_int(cells[8]))
        data['LTP'].append(cells[9])
        data['Previous_Day_Close_Price_Rs'].append(safe_float(cells[10]))
        data['Average_Traded_Price_Rs'].append(safe_float(cells[11]))
        data['Fifty_Two_Week_High_Rs'].append(safe_float(cells[12]))
        data['Fifty_Two_Week_Low_Rs'].append(safe_float(cells[13]))
        data['Market_Capitalization_Rs__Amt_in_Millions'].append(safe_float(cells[14]))
        data['Close_Date'].append(datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d"))

    return pd.DataFrame(data)

def process_html_to_dataframe_symbol(html_content, date_str):

    """Processes HTML content to extract stock data and return as a DataFrame."""

    root = html.fromstring(html_content)
    data = {
        'Symbol': [],
        'Close_Price_Rs': [],
        'Open_Price_Rs': [],
        'High_Price_Rs': [],
        'Low_Price_Rs': [],
        'Total_Traded_Quantity': [],
        'Total_Traded_Value': [],
        'Total_Trades': [],
        'LTP': [],
        'Previous_Day_Close_Price_Rs': [],
        'Average_Traded_Price_Rs': [],
        'Fifty_Two_Week_High_Rs': [],
        'Fifty_Two_Week_Low_Rs': [],
        'Market_Capitalization_Rs__Amt_in_Millions': [],
        'Close_Date': []
    }
        # processing each row in the table
    for row in root.xpath('//table[contains(@class, "table__lg")]/tbody/tr'):
        # ensuring each data list gets a value even if cells are missing
        cells = [cell.text_content().strip() for cell in row.xpath('.//td')]
        if len(cells) != 15:
            continue

        # appending data to each key in the dictionary, converting types as needed
        data['Symbol'].append(cells[1])
        data['Close_Price_Rs'].append(safe_float(cells[2]))
        data['Open_Price_Rs'].append(safe_float(cells[3]))
        data['High_Price_Rs'].append(safe_float(cells[4]))
        data['Low_Price_Rs'].append(safe_float(cells[5]))
        data['Total_Traded_Quantity'].append(safe_int(cells[6]))
        data['Total_Traded_Value'].append(safe_float(cells[7]))
        data['Total_Trades'].append(safe_int(cells[8]))
        data['LTP'].append(cells[9])
        data['Previous_Day_Close_Price_Rs'].append(safe_float(cells[10]))
        data['Average_Traded_Price_Rs'].append(safe_float(cells[11]))
        data['Fifty_Two_Week_High_Rs'].append(safe_float(cells[12]))
        data['Fifty_Two_Week_Low_Rs'].append(safe_float(cells[13]))
        data['Market_Capitalization_Rs__Amt_in_Millions'].append(safe_float(cells[14]))
        data['Close_Date'].append(datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d"))

    return pd.DataFrame(data)

def safe_float(value):

    """
    Safely converts a string to a float. If the conversion fails, returns 0.0. 
    Removes commas and replaces dashes with zeros to handle common numeric formats in data tables.
    """

    try:
        return float(value.replace(',', '').replace('-', '0'))
    except ValueError:
        return 0.0
    
def safe_int(value):

    """
    Safely converts a string to an integer. If the conversion fails, returns 0.
    Removes commas and replaces dashes with zeros to handle common numeric formats in data tables.
    """

    try:
        return int(value.replace(',', '').replace('-', '0'))
    except ValueError:
        return 0