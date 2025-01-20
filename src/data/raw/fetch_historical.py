import requests
import mysql.connector
import time
import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',  # Change to your MySQL host
    'user': 'root',       # Change to your MySQL username
    'password': 'kumartarun', # Change to your MySQL password
    'database': 'data',  # Change to your database name
}

# Binance API endpoint
BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

def fetch_ohlcv(symbol, interval, start_time, end_time):
    """
    Fetch OHLCV data from Binance.
    """
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # Binance API limit per request
    }
    response = requests.get(BINANCE_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def reset_table(cursor, table_name):
    """
    Truncate the table to remove all existing data.
    """
    truncate_query = f"TRUNCATE TABLE {table_name}"
    cursor.execute(truncate_query)

def insert_into_db(data, table_name):
    """
    Insert data into the database.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Create table if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        open_time BIGINT PRIMARY KEY,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        close_time BIGINT
    )
    """
    cursor.execute(create_table_query)

    # Truncate table before inserting new data
    reset_table(cursor, table_name)

    # Insert data into table
    insert_query = f"""
    INSERT INTO {table_name} (open_time, open, high, low, close, volume, close_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, data)
    connection.commit()
    cursor.close()
    connection.close()

def main():
    symbol = "BTCUSDT"
    interval = "1h"
    start_time = int(time.mktime(datetime.datetime(2024, 12, 1).timetuple()) * 1000)
    end_time = int(time.time() * 1000)  # Current timestamp in milliseconds
    table_name = "btc_ohlcv_hourly"

    print(f"Fetching data for {symbol} from {datetime.datetime.fromtimestamp(start_time / 1000)} to now.")
    
    # Fetch data
    ohlcv = fetch_ohlcv(symbol, interval, start_time, end_time)

    # Transform data for insertion
    formatted_data = [
        (
            entry[0],  # open_time
            float(entry[1]),  # open
            float(entry[2]),  # high
            float(entry[3]),  # low
            float(entry[4]),  # close
            float(entry[5]),  # volume
            entry[6]  # close_time
        )
        for entry in ohlcv
    ]

    # Insert into DB
    insert_into_db(formatted_data, table_name)

    print("Data fetching and insertion completed. Table reset and updated.")

if __name__ == "__main__":
    main()
