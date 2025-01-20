import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.dates as mdates
import numpy as np


btc_data = yf.download('BTC-USD', start='2023-12-01', end='2025-01-10', interval='1d')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  


btc_data['Volatility'] = btc_data['Pct_Change'].rolling(window=7).std()


btc_data.dropna(subset=['Pct_Change', 'Volatility'], inplace=True)


btc_data['Date'] = btc_data.index
btc_data['Date_Num'] = mdates.date2num(btc_data['Date'])  


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')


scatter = ax.scatter(
    btc_data['Pct_Change'],  
    btc_data['Volume'],      
    btc_data['Date_Num'],    
    c=btc_data['Volatility'],  
    cmap='rainbow',          
    alpha=0.7
)


ax.zaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: mdates.num2date(value).strftime('%Y-%m-%d')))


ax.set_xlabel('Percentage Change in Price (%)', fontsize=12)
ax.set_ylabel('Volume', fontsize=12)
ax.set_zlabel('Date (Time)', fontsize=12)
cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('Volatility', fontsize=12)


ax.set_title('BTC-USD Price Change vs Volume vs Time (Colored by Volatility)', fontsize=14)


plt.tight_layout()
plt.show()
