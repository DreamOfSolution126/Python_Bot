from flask import Flask, request, jsonify
from mexc_sdk import Spot
import requests
import hmac
import hashlib
import time

app = Flask(__name__)

MEXC_API_KEY = 'mx0vglOnYNH4ePuVvR'
MEXC_API_SECRET = '3a1fa8c0cc7b4a539aa46cf6bad75f53'
BASE_URL = 'https://api.mexc.com' 

spot = Spot(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)

def generate_signature(params):
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    return hmac.new(MEXC_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def place_order(symbol, side, quantity):
    endpoint = '/order'
    params = {
        'symbol': symbol,
        'side': side,  # 'buy' or 'sell'
        'type': 'market', 
        'quantity': quantity,
        'timestamp': int(time.time() * 1000)
    }
    params['signature'] = generate_signature(params)

    headers = {
        'X-MXC-APIKEY': MEXC_API_KEY
    }
    
    response = requests.post(BASE_URL + endpoint, headers=headers, params=params)
    return response.json()

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    print(f"Received data: {data}")  

    signal = data.get('signal')
    symbol = "BTC_USDT"  
    quantity = 0.01  #

    if signal == 'buy':
        order_response = place_order(symbol, 'buy', quantity)
        return jsonify({'status': 'success', 'data': order_response}), 200
    elif signal == 'sell':
        order_response = place_order(symbol, 'sell', quantity)
        return jsonify({'status': 'success', 'data': order_response}), 200

    return jsonify({'status': 'error', 'message': 'Invalid signal'}), 400

if __name__ == '__main__':
    app.run(port=5000)  
