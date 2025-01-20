import yfinance as yf
import matplotlib.pyplot as plt
import pywt
import numpy as np


btc_data = yf.download('BTC-USD', start='2024-11-27', end='2024-12-10', interval='1h')


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


def plot_fft(signal, title):
    
    N = len(signal)
    fft_result = np.fft.fft(signal)
    freqs = np.fft.fftfreq(N)

    
    plt.plot(freqs[:N // 2], np.abs(fft_result)[:N // 2])  
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.grid()


plt.figure(figsize=(14, 10))


plt.subplot(4, 1, 1)
plot_fft(data, 'FFT of Original Signal')


plt.subplot(4, 1, 2)
plot_fft(approximation[:len(btc_data.index)], 'FFT of Low-Frequency Component')


plt.subplot(4, 1, 3)
plot_fft(detail_mid[:len(btc_data.index)], 'FFT of Mid-Frequency Component')


plt.subplot(4, 1, 4)
plot_fft(detail_high[:len(btc_data.index)], 'FFT of High-Frequency Component')

plt.tight_layout()
plt.show()
