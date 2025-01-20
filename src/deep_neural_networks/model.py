import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import time
import threading
from preprocess import fetch_data_from_mysql 
from preprocess import preprocess_data

# Function to create an LSTM model
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=64, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='sigmoid'))  # For binary classification (support/resistance)
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Real-time data fetching and prediction loop
def real_time_prediction(model_support, model_resistance):
    while True:
        # Fetch the latest data
        df = fetch_data_from_mysql()
        
        # Preprocess the new data
        X, y_support, y_resistance, scaler = preprocess_data(df)
        
        # Make predictions using the model
        predictions_support = model_support.predict(X[-1:])
        predictions_resistance = model_resistance.predict(X[-1:])
        
        # Convert predictions to binary values (0 or 1)
        prediction_support_binary = (predictions_support > 0.5).astype(int)
        prediction_resistance_binary = (predictions_resistance > 0.5).astype(int)
        
        # Output predictions
        print(f"Predicted Support: {prediction_support_binary}, Predicted Resistance: {prediction_resistance_binary}")
        
        # Wait for 5 seconds before fetching new data
        time.sleep(5)

# To run in a separate thread for real-time predictions
def start_real_time_prediction(model_support, model_resistance):
    prediction_thread = threading.Thread(target=real_time_prediction, args=(model_support, model_resistance))
    prediction_thread.start()
