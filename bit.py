import requests
import matplotlib.pyplot as plt
from datetime import datetime


def fetch_funding_rates(symbol="XBTUSD", count=500):
    """
    Fetch historical funding rates for a given symbol from BitMEX API.
    
    :param symbol: Perpetual contract symbol (e.g., "XBTUSD").
    :param count: Number of data points to fetch (max: 500).
    :return: A list of dictionaries containing timestamps and funding rates.
    """
    url = "https://www.bitmex.com/api/v1/funding"
    params = {"symbol": symbol, "count": count, "reverse": True}  
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return []


def plot_funding_rates(funding_data):
    """
    Plot funding rates using Matplotlib.
    
    :param funding_data: List of dictionaries with timestamps and funding rates.
    """
    if not funding_data:
        print("No data to plot.")
        return
    
    
    timestamps = [datetime.strptime(entry['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ") for entry in funding_data]
    funding_rates = [entry['fundingRate'] for entry in funding_data]
    
    
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, funding_rates, marker="o", linestyle="-", color="b", label="Funding Rate")
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8, label="Neutral Funding Rate")
    
    
    plt.title("BitMEX Funding Rates Over Time", fontsize=14)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Funding Rate", fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    
    plt.show()


if __name__ == "__main__":
    
    funding_data = fetch_funding_rates(symbol="XBTUSD", count=50)
    
    
    plot_funding_rates(funding_data)
