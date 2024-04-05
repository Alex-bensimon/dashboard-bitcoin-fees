import requests
import json
import pandas as pd
from datetime import datetime

def get_binance_historical_data(symbol, interval, start_time=None, end_time=None, limit=1000):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    if start_time:
        url += f"&startTime={int(start_time.timestamp() * 1000)}"
    if end_time:
        url += f"&endTime={int(end_time.timestamp() * 1000)}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        return None

# Example usage:
symbol = 'BTCUSDT'  # Symbol for Bitcoin-USDT pair
interval = '1d'     # Interval: 1 day
start_time = datetime(2017, 8, 17)  # Start time for historical data
end_time = datetime.now()    # End time for historical data (optional)
btc_data = []

# Fetch data in chunks of 1000 data points
while start_time < end_time if end_time else True:
    data_chunk = get_binance_historical_data(symbol, interval, start_time=start_time, end_time=end_time)
    if data_chunk is None:
        break
    btc_data.extend(data_chunk)
    start_time = datetime.fromtimestamp(int(data_chunk[-1][0]) / 1000) + pd.Timedelta(days=1)  # Increment start_time for the next request

# Write data to a JSON file
with open('btc_historical_data.json', 'w') as json_file:
    json.dump(btc_data, json_file)

print("Data saved to btc_historical_data.json")
import Calculate_mean_price 
print("BTC mean prices are loaded in btc_mean_prices")
