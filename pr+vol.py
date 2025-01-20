import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


btc_data = yf.download('BTC-USD', start='2024-12-20', end='2025-01-10', interval='1h')


btc_data['Pct_Change'] = (btc_data['Close'].pct_change() * 100)  


btc_data.dropna(subset=['Pct_Change'], inplace=True)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)


ax1.plot(btc_data.index, btc_data['Pct_Change'], label='BTC-USD Hourly % Change', color='tab:blue')
ax1.set_title('BTC-USD Hourly Percentage Change Over Time')
ax1.set_ylabel('Percentage Change (%)')
ax1.grid(True)
ax1.legend()


ax2.plot(btc_data.index, btc_data['Volume'], label='BTC-USD Hourly Volume', color='tab:orange')
ax2.set_title('BTC-USD Hourly Volume Over Time')
ax2.set_xlabel('Date and Time')
ax2.set_ylabel('Volume')
ax2.grid(True)
ax2.legend()


plt.xticks(rotation=45)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

plt.tight_layout()
plt.show()
