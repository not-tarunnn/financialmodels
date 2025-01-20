import mysql.connector
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


# Function to fetch the latest OHLCV data from MySQL
def fetch_data_from_mysql():
    connection = mysql.connector.connect(
        host="localhost",  # e.g., localhost or your remote host
        user="root",  # e.g., 'root'
        password="kumartarun",
        database="data"
    )
    
    query = "SELECT Open, High, Low, Close, Open_time, Close_time, Volume FROM btc_ohlcv_hourly ORDER BY Close_time DESC LIMIT 1000"  # Modify as needed
    df = pd.read_sql(query, connection)
    
    # Close the connection after fetching the data
    connection.close()
    
    return df

# Function to preprocess the data (feature engineering, scaling, etc.)
def preprocess_data(data, lookback=50):
    # Add technical indicators or moving averages
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # Support and resistance calculations based on rolling windows
    window_size = 50
    data['resistance'] = data['High'].rolling(window=window_size).max()
    data['support'] = data['Low'].rolling(window=window_size).min()
    
    data = data.dropna()
    
    # Scaling the features (Open, High, Low, Close, Volume, SMA)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_10', 'SMA_50']])
    
    # Prepare data for the LSTM model
    X, y_support, y_resistance = prepare_data(data_scaled, data, lookback)
    return X, y_support, y_resistance, scaler

# Function to prepare data for LSTM model (sliding window approach)
def prepare_data(data_scaled, data, lookback=50):
    X = []
    y_support = []
    y_resistance = []
    
    for i in range(lookback, len(data)):
        X.append(data_scaled[i-lookback:i])  # Sequence of 'lookback' time steps
        y_support.append(1 if data['Close'][i] <= data['support'][i] else 0)  # Support label
        y_resistance.append(1 if data['Close'][i] >= data['resistance'][i] else 0)  # Resistance label
        
    X = np.array(X)
    y_support = np.array(y_support)
    y_resistance = np.array(y_resistance)
    
    return X, y_support, y_resistance


