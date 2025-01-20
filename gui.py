import yfinance as yf
import pywt
import numpy as np
from playsound import playsound  
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel 
from PyQt5.QtGui import QFont
import sys
import math


slope_low = 0
slope_mid = 0
slope_high = 0
data = []
percent_change = 0


def fetch_data():
    global data, percent_change

    
    btc_data = yf.download('BTC-USD', start='2024-10-25', end='2024-12-10', interval='1d') 
    btc_data['Pct_Change'] = btc_data['Close'].pct_change() * 100  
    btc_data.dropna(subset=['Pct_Change'], inplace=True)  
    data = btc_data['Pct_Change'].values  

    
    if len(btc_data) > 0:
        percent_change = btc_data['Pct_Change'].iloc[-1]


def compute_slope(component):
    return abs(component[-1] - component[-2])  


def compute_wavelet_slopes():
    global slope_low, slope_mid, slope_high, data

    if len(data) < 2:  
        return

    
    wavelet = 'db4'
    level = 3
    coeffs = pywt.wavedec(data, wavelet, level=level)  

    cA3, cD3, cD2, cD1 = coeffs  

    
    approximation = pywt.waverec([cA3] + [None] * 3, wavelet)  
    detail_high = pywt.waverec([cD1] + [None] * 3, wavelet)  
    detail_mid = pywt.waverec([cD2] + [None] * 3, wavelet)  

    
    slope_low = compute_slope(approximation)
    slope_mid = compute_slope(detail_mid)
    slope_high = compute_slope(detail_high)


class SlopeDisplayApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BTC-USD Slope Monitor")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        
        self.layout = QVBoxLayout()

        
        self.low_slope_label = QLabel(f"Low-Frequency Slope: {slope_low:.4f}°", self)
        self.mid_slope_label = QLabel(f"Mid-Frequency Slope: {slope_mid:.4f}°", self)
        self.high_slope_label = QLabel(f"High-Frequency Slope: {slope_high:.4f}°", self)
        self.pct_change_label = QLabel(f"Percentage Change: {percent_change:.4f}%", self)

        
        font = QFont('Tahoma', 14)  
        self.low_slope_label.setFont(font)
        self.mid_slope_label.setFont(font)
        self.high_slope_label.setFont(font)
        self.pct_change_label.setFont(font)

        
        self.layout.addWidget(self.low_slope_label)
        self.layout.addWidget(self.mid_slope_label)
        self.layout.addWidget(self.high_slope_label)
        self.layout.addWidget(self.pct_change_label)

        
        self.setLayout(self.layout)

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_slopes)
        self.timer.start(1000)  

    def refresh_slopes(self):
        global slope_low, slope_mid, slope_high

        
        fetch_data()
        compute_wavelet_slopes()

        
        slope_low_deg = math.degrees(slope_low)
        slope_mid_deg = math.degrees(slope_mid)
        slope_high_deg = math.degrees(slope_high)

        
        self.low_slope_label.setText(f"Low-Frequency Slope: {slope_low_deg:.4f}°")
        self.mid_slope_label.setText(f"Mid-Frequency Slope: {slope_mid_deg:.4f}°")
        self.high_slope_label.setText(f"High-Frequency Slope: {slope_high_deg:.4f}°")
        self.pct_change_label.setText(f"Percentage Change: {percent_change:.4f}%")

    
        
        
        
        



if __name__ == '__main__':
    
    fetch_data()
    compute_wavelet_slopes()

    
    app = QApplication(sys.argv)
    window = SlopeDisplayApp()
    window.show()
    app.exec_()
