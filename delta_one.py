import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
btc_data = yf.download('BTC-USD', start='2024-11-10', end='2024-11-20', interval='1d')
btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  
btc_data.dropna(subset=['Pct_Change'], inplace=True)
plt.figure(figsize=(12, 6))
plt.plot(btc_data.index, btc_data['Pct_Change'], label='BTC-USD Hourly % Change', color='tab:blue')
plt.title('BTC-USD Hourly Percentage Change Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Percentage Change (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  
plt.tight_layout()
plt.legend()
plt.show()
