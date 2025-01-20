import yfinance as yf
import pywt
import numpy as np
import time

while True:
    
    btc_data = yf.download('BTC-USD', start='2024-12-01', end='2024-12-30', interval='1h')

    
    btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  
    btc_data.dropna(subset=['Pct_Change'], inplace=True)  

    
    data = btc_data['Pct_Change'].values

    
    wavelet = 'db4'  
    level = 3  
    coeffs = pywt.wavedec(data, wavelet, level=level)  

    
    cA3, cD3, cD2, cD1 = coeffs  

    
    approximation = pywt.waverec([cA3] + [None] * 3, wavelet)  
    detail_high = pywt.waverec([cD1] + [None] * 3, wavelet)  
    detail_mid = pywt.waverec([cD2] + [None] * 3, wavelet)  

    
    approximation = approximation[:len(data)]
    detail_high = detail_high[:len(data)]
    detail_mid = detail_mid[:len(data)]

    
    latest_low_freq = approximation[-1]
    latest_mid_freq = detail_mid[-1]
    latest_high_freq = detail_high[-1]

    
    print("\033c", end="")  

    
    print(f" Low-Frequency Value: {latest_low_freq:.2f}%")
    print(f" Mid-Frequency Value: {latest_mid_freq:.2f}%")
    print(f" High-Frequency Value: {latest_high_freq:.2f}%")

    
    time.sleep(5)
