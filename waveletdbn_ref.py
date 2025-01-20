import yfinance as yf
import matplotlib.pyplot as plt
import pywt
import numpy as np
from matplotlib.animation import FuncAnimation


def fetch_data():
    btc_data = yf.download('BTC-USD', start='2024-12-01', end='2025-01-30', interval='1h')
    btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  
    btc_data.dropna(subset=['Pct_Change'], inplace=True)  
    return btc_data


def perform_wavelet_decomposition(data):
    wavelet = 'db4'  
    level = 3  
    coeffs = pywt.wavedec(data, wavelet, level=level)
    cA3, cD3, cD2, cD1 = coeffs  
    approximation = pywt.waverec([cA3] + [None]*3, wavelet)  
    detail_high = pywt.waverec([cD1] + [None]*3, wavelet)  
    detail_mid = pywt.waverec([cD2] + [None]*3, wavelet)  
    return approximation, detail_mid, detail_high


def update_plot(frame):
    
    btc_data = fetch_data()
    data = btc_data['Pct_Change'].values
    approximation, detail_mid, detail_high = perform_wavelet_decomposition(data)
    
    
    for ax in axs:
        ax.clear()
    
    
    axs[0].plot(btc_data.index, data, label='Original Percentage Change', color='blue')
    axs[0].set_title('Original Percentage Change Signal')
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(btc_data.index, approximation[:len(btc_data.index)], label='Low-Frequency Trend', color='green')
    axs[1].set_title('Low-Frequency Component (Trend)')
    axs[1].legend()
    axs[1].grid()

    axs[2].plot(btc_data.index, detail_mid[:len(btc_data.index)], label='Mid-Frequency Fluctuations', color='orange')
    axs[2].set_title('Mid-Frequency Component')
    axs[2].legend()
    axs[2].grid()

    axs[3].plot(btc_data.index, detail_high[:len(btc_data.index)], label='High-Frequency Noise', color='red')
    axs[3].set_title('High-Frequency Component (Noise)')
    axs[3].legend()
    axs[3].grid()

    plt.tight_layout()


fig, axs = plt.subplots(4, 1, figsize=(12, 8))


ani = FuncAnimation(fig, update_plot, interval=5000)  

plt.show()
