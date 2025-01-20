import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fetch historical BTC/USD data from Yahoo Finance
btc_data = yf.download('BTC-USD', start='2020-01-01', end='2025-01-01')

# Calculate daily returns
btc_data['returns'] = btc_data['Adj Close'].pct_change() * 100  # Returns in percentage

# Calculate rolling volatility for 9-day, 14-day, and 21-day windows
btc_data['9_day_volatility'] = btc_data['returns'].rolling(window=9).std()
btc_data['14_day_volatility'] = btc_data['returns'].rolling(window=14).std()
btc_data['21_day_volatility'] = btc_data['returns'].rolling(window=21).std()

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(btc_data.index, btc_data['9_day_volatility'], label='9-Day Rolling Volatility', color='blue')
plt.plot(btc_data.index, btc_data['14_day_volatility'], label='14-Day Rolling Volatility', color='green')
plt.plot(btc_data.index, btc_data['21_day_volatility'], label='21-Day Rolling Volatility', color='red')

plt.title('Rolling Volatility of BTC/USD (9-day, 14-day, 21-day)')
plt.xlabel('Date')
plt.ylabel('Volatility (%)')
plt.legend(loc='best')
plt.show()

# Display the latest volatility values
latest_9_day_volatility = btc_data['9_day_volatility'].iloc[-1]
latest_14_day_volatility = btc_data['14_day_volatility'].iloc[-1]
latest_21_day_volatility = btc_data['21_day_volatility'].iloc[-1]

print(f"Latest 9-day volatility: {latest_9_day_volatility:.2f}%")
print(f"Latest 14-day volatility: {latest_14_day_volatility:.2f}%")
print(f"Latest 21-day volatility: {latest_21_day_volatility:.2f}%")
