import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


btc_data = yf.download('BTC-USD', start='2024-09-26', end='2024-11-26', interval='1d')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  


btc_data.dropna(subset=['Pct_Change'], inplace=True)


btc_data['Date'] = btc_data.index
btc_data['Date_Num'] = mdates.date2num(btc_data['Date'])  


plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    btc_data['Pct_Change'], 
    btc_data['Volume'], 
    c=btc_data['Date_Num'], 
    cmap='rainbow',  
    alpha=0.7
)


cbar = plt.colorbar(scatter)
cbar.set_label('Date', fontsize=12)


def format_func(value, tick_number):
    date = mdates.num2date(value)  
    return date.strftime('%Y-%m-%d %H:%M')

cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))


plt.title('BTC-USD Price Change vs Volume with VIBGYOR Time Dimension', fontsize=14)
plt.xlabel('Percentage Change in Price (%)', fontsize=12)
plt.ylabel('Volume', fontsize=12)


plt.grid(True)


plt.tight_layout()
plt.show()
