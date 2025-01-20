import yfinance as yf
import matplotlib.pyplot as plt
import pywt
import numpy as np


btc_data = yf.download('BTC-USD', start='2024-12-30', end='2025-01-11', interval='1h')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  
btc_data.dropna(subset=['Pct_Change'], inplace=True)  



data = btc_data['Pct_Change'].values


wavelet = 'db4'  
level = 3  
coeffs = pywt.wavedec(data, wavelet, level=level)  



cA3, cD3, cD2, cD1 = coeffs  


approximation = pywt.waverec([cA3] + [None]*3, wavelet)  
detail_high = pywt.waverec([cD1] + [None]*3, wavelet)  
detail_mid = pywt.waverec([cD2] + [None]*3, wavelet)  


plt.figure(figsize=(12, 8))


plt.subplot(4, 1, 1)
plt.plot(btc_data.index, data, label='Original Percentage Change', color='blue')
plt.title('Original Percentage Change Signal')
plt.legend()
plt.grid()


plt.subplot(4, 1, 2)
plt.plot(btc_data.index, approximation[:len(btc_data.index)], label='Low-Frequency Trend', color='green')
plt.title('Low-Frequency Component (Trend)')
plt.legend()
plt.grid()


plt.subplot(4, 1, 3)
plt.plot(btc_data.index, detail_mid[:len(btc_data.index)], label='Mid-Frequency Fluctuations', color='orange')
plt.title('Mid-Frequency Component')
plt.legend()
plt.grid()


plt.subplot(4, 1, 4)
plt.plot(btc_data.index, detail_high[:len(btc_data.index)], label='High-Frequency Noise', color='red')
plt.title('High-Frequency Component (Noise)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

