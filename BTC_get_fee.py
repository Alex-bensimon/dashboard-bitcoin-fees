import os
import json
import requests
from datetime import datetime

def get_btc_fee():
    url = 'https://api.blockchain.info/mempool/fees'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Add the day's date to the data
            today = datetime.now().strftime("%Y-%m-%d")
            data['date'] = today
            return data
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_to_json(data):
    # Check if JSON file for today's date already exists
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"btc_fee_{today}.json"
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(data, f)
            print(f"Data saved to {filename}")
    else:
        print(f"Data for {today} already exists.")

if __name__ == "__main__":
    btc_fee = get_btc_fee()
    if btc_fee:
        save_to_json(btc_fee)
