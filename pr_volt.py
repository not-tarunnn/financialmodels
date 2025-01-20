import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


btc_data = yf.download('BTC-USD', start='2024-11-1', end='2024-12-30', interval='1hani')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  


rolling_window = 5  
btc_data['Volatility'] = btc_data['Pct_Change'].rolling(window=rolling_window).std()


btc_data.dropna(subset=['Pct_Change', 'Volatility'], inplace=True)


plt.figure(figsize=(14, 8))


plt.subplot(2, 1, 1)
plt.plot(btc_data.index, btc_data['Pct_Change'], label='BTC-USD % Change', color='tab:blue')
plt.title('BTC-USD Percentage Change Over Time')
plt.xlabel('Date')
plt.ylabel('Percentage Change (%)')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)


plt.subplot(2, 1, 2)
plt.plot(btc_data.index, btc_data['Volatility'], label=f'{rolling_window}-Day Rolling Volatility', color='tab:orange')
plt.title('BTC-USD Rolling Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility (Standard Deviation)')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()


plt.show()
