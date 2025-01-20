import json
import time
from datetime import datetime, timedelta
import mysql.connector
from websocket import WebSocketApp

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kumartarun',
    'database': 'data',
}

# Binance WebSocket URL
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"

def get_last_hour_start():
    """
    Retrieves the open_time of the most recent data point in the database.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Query the latest record
    query = "SELECT open_time FROM btc_ohlcv_hourly ORDER BY open_time DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    # If no data exists, return None
    return result[0] if result else None

def insert_new_datapoint():
    """
    Inserts a new data point based on the next hour after the latest record.
    """
    last_open_time = get_last_hour_start()

    # If no previous data exists, start from the current hour
    if last_open_time is None:
        next_hour_start = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    else:
        next_hour_start = datetime.utcfromtimestamp(last_open_time / 1000) + timedelta(hours=1)

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # SQL query to insert a new hourly datapoint
    insert_query = """
    INSERT INTO btc_ohlcv_hourly (open_time, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    # Initialize with placeholder values
    cursor.execute(insert_query, (
        int(next_hour_start.timestamp() * 1000),  # Open time in milliseconds
        None,  # Open price (to be updated later)
        None,  # High price (to be updated later)
        None,  # Low price (to be updated later)
        None,  # Close price (to be updated later)
        0,     # Volume (initially 0)
    ))

    connection.commit()
    cursor.close()
    connection.close()
    print(f"New datapoint created for {next_hour_start}.")

def update_latest_point(data):
    """
    Updates the latest data point in the database with real-time data.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # SQL query to update the latest data point
    update_query = """
    UPDATE btc_ohlcv_hourly
    SET high = GREATEST(IFNULL(high, %s), %s),
        low = LEAST(IFNULL(low, %s), %s),
        close = %s,
        volume = volume + %s
    WHERE open_time = %s
    """
    cursor.execute(update_query, (
        data['high'],
        data['high'],
        data['low'],
        data['low'],
        data['close'],
        data['volume'],
        data['open_time']
    ))

    connection.commit()
    cursor.close()
    connection.close()

def on_message(ws, message):
    """
    Handle incoming WebSocket messages.
    """
    parsed_message = json.loads(message)
    kline = parsed_message['k']

    # Extract required fields
    data = {
        'open_time': kline['t'],  # Open time
        'high': float(kline['h']),  # High price
        'low': float(kline['l']),  # Low price
        'close': float(kline['c']),  # Close price
        'volume': float(kline['v']),  # Volume
    }

    print(f"Real-time update: {data}")
    update_latest_point(data)

    # Check if the last recorded hour has passed
    last_open_time = get_last_hour_start()
    if last_open_time and datetime.utcnow() >= datetime.utcfromtimestamp(last_open_time / 1000) + timedelta(hours=1):
        insert_new_datapoint()

def on_error(ws, error):
    """
    Handle WebSocket errors.
    """
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """
    Handle WebSocket closure.
    """
    print("WebSocket closed")

def on_open(ws):
    """
    Handle WebSocket connection opening.
    """
    print("WebSocket connection opened")

def main():
    # Initialize the first hourly data point if not already in the database
    insert_new_datapoint()

    ws = WebSocketApp(
        BINANCE_WS_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    main()
