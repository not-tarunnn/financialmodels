from sqlalchemy import create_engine
import pandas as pd
import pywt
import numpy as np
import os
import time

# Database configuration
DB_CONFIG = {
    'user': 'root',
    'password': 'kumartarun',
    'host': 'localhost',
    'database': 'data',
}

# SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

def fetch_data():
    """
    Fetches OHLCV data from the database.
    """
    query = "SELECT open_time, close FROM btc_ohlcv_hourly ORDER BY open_time ASC"
    data = pd.read_sql(query, engine)
    data['open_time'] = pd.to_datetime(data['open_time'])  # Convert open_time to datetime
    return data

def calculate_slope(series):
    """
    Calculate the slope between the latest 2 end points of a series.
    """
    # Get the last two points in the series
    x1, x2 = len(series) - 2, len(series) - 1
    y1, y2 = series[x1], series[x2]
    
    # Calculate the slope (change in y / change in x)
    slope = (y2 - y1) / (x2 - x1)
    return slope

def clear_terminal():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def analyze_data():
    """
    Function to fetch data, analyze it with wavelet decomposition, and print results.
    """
    # Clear terminal before new analysis
    clear_terminal()

    # Step 1: Fetch latest data
    print("Fetching latest data...")
    btc_data = fetch_data()

    # Step 2: Calculate the percentage change in the closing price
    btc_data['Pct_Change'] = btc_data['close'].pct_change() * 100  # Percentage change
    btc_data.dropna(subset=['Pct_Change'], inplace=True)  # Remove NaN values

    # Step 3: Extract the percentage change series
    data = btc_data['Pct_Change'].values

    # Step 4: Perform Wavelet Decomposition using pywt
    wavelet = 'db4'  # Daubechies wavelet of order 4
    level = 3  # Number of decomposition levels
    coeffs = pywt.wavedec(data, wavelet, level=level)  # Decompose into levels

    # Step 5: Separate Approximation and Details
    cA3, cD3, cD2, cD1 = coeffs  # Approximation and details at different levels
    approximation = pywt.waverec([cA3] + [None]*3, wavelet)[:len(data)]  # Low-frequency trend
    detail_mid = pywt.waverec([cD2] + [None]*3, wavelet)[:len(data)]  # Mid-frequency component
    detail_high = pywt.waverec([cD1] + [None]*3, wavelet)[:len(data)]  # High-frequency component

    # Print values and slopes
    print("\nLatest Data Analysis:")
    print(f"Original Percentage Change: {data[-1]:.4f}")
    print(f"Low-Frequency Trend Value: {approximation[-1]:.4f}")
    print(f"Mid-Frequency Fluctuation Value: {detail_mid[-1]:.4f}")
    print(f"High-Frequency Noise Value: {detail_high[-1]:.4f}")
    print(f"Original Signal Slope: {calculate_slope(data):.6f}")
    print(f"Low-Frequency Slope: {calculate_slope(approximation):.6f}")
    print(f"Mid-Frequency Slope: {calculate_slope(detail_mid):.6f}")
    print(f"High-Frequency Slope: {calculate_slope(detail_high):.6f}")

def main():
    """
    Main function to periodically analyze data.
    """
    while True:
        analyze_data()
        print("\nWaiting for next update...\n")
        time.sleep(0.5)  # Update every 0.5 seconds

if __name__ == "__main__":
    main()
