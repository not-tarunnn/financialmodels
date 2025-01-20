import requests
import time

# Define the URL for the Fear and Greed Index API
url = "https://api.alternative.me/fng/"

# Function to fetch Fear and Greed Index
def fetch_fear_greed_index():
    try:
        # Make a request to the API
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()
            
            # Extract the latest Fear and Greed Index
            fear_greed_index = data['data'][0]['value']
            fear_greed_value = data['data'][0]['value_classification']
            timestamp = data['data'][0]['timestamp']
            
            print(f"Fear and Greed Index: {fear_greed_index} ({fear_greed_value})")
            print(f"Timestamp: {timestamp}")
        else:
            print(f"Error fetching data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Continuously fetch the Fear and Greed Index every 5 minutes
while True:
    fetch_fear_greed_index()
    
    # Wait for 5 minutes (300 seconds) before making the next request
    time.sleep(300)
