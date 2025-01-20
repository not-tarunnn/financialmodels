#made by tarun
import websocket
import pymysql
import json
import numpy as np
from collections import defaultdict
import tensorflow as tf
import tensorflow_probability as tfp
from tabulate import tabulate


DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'hmm'


states = {
    'G1': "Continuation Bullish Candle",
    'G2': "Doji",
    'G3': "Bearish Candle",
    'G4': "Engulfing Bearish Candle",
    'G5': "Inverted Hammer",
    'R1': "Continuation Bearish Candle",
    'R2': "Doji",
    'R3': "Bullish Candle",
    'R4': "Engulfing Bullish Candle",
    'R5': "Shooting Star"
}
transition_counts = defaultdict(lambda: defaultdict(int))


def determine_state(open_price, close_price, prev_close, prev_high, prev_low):
    """
    Determines the state of the candle based on its open and close prices
    relative to the previous candle's prices.
    
    Args:
    - open_price: The opening price of the current candle.
    - close_price: The closing price of the current candle.
    - prev_close: The closing price of the previous candle.
    - prev_high: The high price of the previous candle.
    - prev_low: The low price of the previous candle.
    
    Returns:
    - A string representing the state of the candle.
    """
    
    if open_price > prev_close and close_price > prev_high:
        return 'G1'  
    elif open_price < prev_close and open_price > prev_close and close_price < prev_high:
        return 'G2'  
    elif open_price > prev_close and close_price < open_price:
        return 'G3'  
    elif open_price > prev_high and close_price < prev_low:
        return 'G4'  
    elif open_price < prev_close and close_price < prev_low:
        return 'G5'  

    
    elif open_price < prev_close and close_price < prev_low:
        return 'R1'  
    elif open_price > prev_close and open_price < prev_high and close_price < prev_close:
        return 'R2'  
    elif open_price < prev_close and close_price > open_price:
        return 'R3'  
    elif open_price < prev_low and close_price > prev_high:
        return 'R4'  
    elif open_price > prev_close and close_price < prev_close:
        return 'R5'  

    return None  



def build_hmm_model(transition_matrix):
    num_states = len(states)
   
    initial_distribution = np.ones(num_states) / num_states
    
    transition_distribution = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)
    
    
    
    hmm_model = tfp.distributions.HiddenMarkovModel(
        initial_distribution=tf.constant(initial_distribution, dtype=tf.float32),
        transition_distribution=tfp.distributions.Categorical(probs=tf.constant(transition_distribution, dtype=tf.float32)),
        emission_distribution=tfp.distributions.Categorical(probs=tf.constant(np.eye(num_states), dtype=tf.float32)),
        num_steps=1)

    return hmm_model


def get_transition_matrix():
    num_states = len(states)
    transition_matrix = np.zeros((num_states, num_states))

    for prev_state, next_states in transition_counts.items():
        for next_state, count in next_states.items():
            transition_matrix[int(prev_state[1]) - 1][int(next_state[1]) - 1] += count

    return transition_matrix
 

def predict_next_state(current_state, transition_matrix):
    current_index = int(current_state[1]) - 1  
    transition_probabilities = transition_matrix[current_index]
    next_state_index = np.argmax(transition_probabilities)
    next_state = f"{'G' if next_state_index < 5 else 'R'}{next_state_index + 1}"
    return next_state


def store_data(data):
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()
    
    
    insert_query = "INSERT INTO btcdata (open, close, high, low, timestamp) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (data['o'], data['c'], data['h'], data['l'], data['t']))
    
    connection.commit()
    cursor.close()
    connection.close()

def fetch_previous_state():
    """
    Fetches the most recent previous state from the previous_states table.
    
    Returns:
    - A tuple containing (current_state, previous_state) or (None, None) if no data is found.
    """
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()
    
    try:
        query = "SELECT current_state, previous_state FROM previous_states ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()  

        if result:
            return result  
        else:
            return None, None  
    finally:
        cursor.close()
        connection.close()

def fetch_previous_candle():
    """
    Fetches the most recent candle data from the btcdata table.
    
    Returns:
    - A tuple containing (prev_open, prev_close, prev_high, prev_low) or (None, None, None, None) if no data is found.
    """
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()
    
    try:
        query = "SELECT open, close, high, low FROM btcdata ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()  

        if result:
            return result  
        else:
            return None, None, None, None  
    finally:
        cursor.close()
        connection.close()
def store_previous_state(current_state, previous_state, timestamp):
    """
    Stores the current and previous state in the previous_states table.
    
    Args:
    - current_state: The current state of the candle.
    - previous_state: The previous state of the candle.
    - timestamp: The timestamp of the current candle.
    """
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()
    
    try:
        query = "INSERT INTO previous_states (current_state, previous_state, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(query, (current_state, previous_state, timestamp))
        connection.commit()  
    finally:
        cursor.close()
        connection.close()
        


def on_message(ws, message):
    global previous_state
    
    msg = json.loads(message)
    candle = msg['k']
    
     
    if candle['x']:  
        open_price = float(candle['o'])
        close_price = float(candle['c'])
        high_price = float(candle['h'])
        low_price = float(candle['l'])
        timestamp = candle['t']
    
    
    store_data(candle)
    
    
    prev_open, prev_close, prev_high, prev_low = fetch_previous_candle()
    
    
    current_state = determine_state(open_price, close_price, prev_close, prev_high, prev_low)
    
    
    if current_state:
        if previous_state:  
            transition_counts[previous_state][current_state] += 1
            
            
            store_previous_state(current_state, previous_state, timestamp)
        
        
        transition_matrix = get_transition_matrix()  
        predicted_next_state = predict_next_state(current_state, transition_matrix)
        
        
        print(f"Current State: {current_state}, Predicted Next State: {predicted_next_state}")
        
        
        previous_state = current_state


def start_websocket():
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@kline_1m",
                                on_message=on_message)
    ws.run_forever()


if __name__ == "__main__":
  
    previous_state, _ = fetch_previous_state()
    
    start_websocket()



