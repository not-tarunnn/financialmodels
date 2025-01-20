import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


btc_data = yf.download('BTC-USD', start='2024-11-16', end='2024-11-30', interval='1d')


btc_data['Pct_Change'] = (btc_data['Close'].pct_change() * 100)  


btc_data.dropna(subset=['Pct_Change'], inplace=True)


btc_data['Pct_Change_Derivative'] = (btc_data['Pct_Change'].diff())  


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15), sharex=True)


ax1.plot(btc_data.index, btc_data['Pct_Change'], label='BTC-USD Hourly % Change', color='tab:blue')
ax1.set_title('BTC-USD Hourly Percentage Change Over Time')
ax1.set_ylabel('Percentage Change (%)')
ax1.grid(True)
ax1.legend()


ax2.plot(btc_data.index, btc_data['Pct_Change_Derivative'], label='Derivative of Percentage Change', color='tab:green')
ax2.set_title('Derivative of BTC-USD Hourly Percentage Change Over Time')
ax2.set_ylabel('Rate of Change (%)')
ax2.grid(True)
ax2.legend()


ax3.plot(btc_data.index, btc_data['Volume'], label='BTC-USD Hourly Volume', color='tab:orange')
ax3.set_title('BTC-USD Hourly Volume Over Time')
ax3.set_xlabel('Date and Time')
ax3.set_ylabel('Volume')
ax3.grid(True)
ax3.legend()


plt.xticks(rotation=45)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))


plt.tight_layout()


plt.show()
