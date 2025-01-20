import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


btc_data = yf.download('BTC-USD', start='2024-11-1', end='2024-11-30', interval='1d')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  


btc_data.dropna(subset=['Pct_Change'], inplace=True)


btc_data['Time'] = pd.to_datetime(btc_data.index).astype('int64') // 10**9  


x = btc_data['Time']  
y = btc_data['Pct_Change']  
z = btc_data['Volume']  


xi = np.linspace(x.min(), x.max(), 50)  
yi = np.linspace(y.min(), y.max(), 50)  
xi, yi = np.meshgrid(xi, yi)  


zi = griddata((x, y), z, (xi, yi), method='cubic')  


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')


surf = ax.plot_surface(xi, yi, zi, cmap='viridis', edgecolor='none', alpha=0.8)


cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Volume', fontsize=12)


ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Percentage Change (%)', fontsize=12)
ax.set_zlabel('Volume', fontsize=12)
ax.set_title('BTC-USD 3D Surface: Price Change vs Volume vs Time', fontsize=14)


ax.view_init(elev=20, azim=30)


plt.tight_layout()
plt.show()
