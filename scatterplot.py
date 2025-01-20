import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


btc_data = yf.download('BTC-USD', start='2024-09-26', end='2024-11-26', interval='1d')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  


btc_data.dropna(subset=['Pct_Change'], inplace=True)


plt.figure(figsize=(10, 6))
plt.scatter(btc_data['Pct_Change'], btc_data['Volume'], alpha=0.5, color='tab:green')


plt.title('BTC-USD Price Change vs Volume', fontsize=14)
plt.xlabel('Percentage Change in Price (%)', fontsize=12)
plt.ylabel('Volume', fontsize=12)


plt.grid(True)


plt.tight_layout()
plt.show()
