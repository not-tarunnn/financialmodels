import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt.style.use('dark_background')


btc_data = yf.download('BTC-USD', start='2024-12-01', end='2024-12-30', interval='1d')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  


btc_data.dropna(subset=['Pct_Change'], inplace=True)


def smooth_non_differentiable(data, threshold=5, window=5):
    """
    Smooth the data only at points where the rate of change is large (non-differentiable).
    
    Parameters:
    - data: The data to smooth.
    - threshold: The rate of change above which a point is considered non-differentiable.
    - window: The window size for smoothing (using a moving average).
    
    Returns:
    - Smoothed data.
    """
    smoothed_data = data.copy()  
    
    
    diff = np.diff(data)
    
    
    non_diff_indices = np.where(np.abs(diff) > threshold)[0]
    
    
    for i in non_diff_indices:
        start = max(i - window // 2, 0)
        end = min(i + window // 2 + 1, len(data))
        smoothed_data[i] = np.mean(data[start:end])
    
    return smoothed_data


btc_data['Pct_Change_Smooth'] = smooth_non_differentiable(btc_data['Pct_Change'], threshold=5, window=5)
btc_data['Volume_Smooth'] = smooth_non_differentiable(btc_data['Volume'], threshold=50000000, window=5)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)


ax1.plot(btc_data.index, btc_data['Pct_Change'], label='BTC-USD Daily % Change (Raw)', color='blue', linestyle='--', alpha=0.6)  
ax1.plot(btc_data.index, btc_data['Pct_Change_Smooth'], label='Smoothed % Change (Non-differentiable Points)', color='orange', linewidth=2)  
ax1.set_title('BTC-USD Daily Percentage Change Over Time', fontsize=14, color='white')
ax1.set_ylabel('Percentage Change (%)', fontsize=12, color='white')
ax1.grid(True, color='green',linestyle='--', alpha=0.6)  
ax1.legend()


ax2.plot(btc_data.index, btc_data['Volume'], label='BTC-USD Daily Volume (Raw)', color='yellow', linestyle='--', alpha=0.6)  
ax2.plot(btc_data.index, btc_data['Volume_Smooth'], label='Smoothed Volume (Non-differentiable Points)', color='white', linewidth=2)  
ax2.set_title('BTC-USD Daily Volume Over Time', fontsize=14, color='white')
ax2.set_xlabel('Date', fontsize=12, color='white')
ax2.set_ylabel('Volume', fontsize=12, color='white')
ax2.grid(True, color='green',linestyle='--', alpha=0.6)  
ax2.legend()


plt.xticks(rotation=45, color='white')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))


fig.patch.set_facecolor('black')

plt.tight_layout()
plt.show()
