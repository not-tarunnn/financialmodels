import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt


btc_data = yf.download('BTC-USD', start='2024-10-19', end='2024-11-30', interval='1d')


btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  


btc_data.dropna(subset=['Pct_Change'], inplace=True)


pct_change = btc_data['Pct_Change'].values  
n = len(pct_change)  


fft_result = np.fft.fft(pct_change)
frequencies = np.fft.fftfreq(n)  


amplitudes = np.abs(fft_result)


plt.figure(figsize=(12, 6))
plt.plot(frequencies[:n // 2], amplitudes[:n // 2], color='tab:orange')  
plt.title('Frequency vs Amplitude (BTC-USD % Change)')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.grid(True)


plt.tight_layout()
plt.show()
