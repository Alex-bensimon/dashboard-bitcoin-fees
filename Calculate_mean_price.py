from collections import defaultdict
import json
from datetime import datetime

def calculate_mean_price(json_data):
    # Create a defaultdict to store data points grouped by day
    grouped_data = defaultdict(list)

    # Iterate through each data point and group by day
    for item in json_data:
        timestamp_ms = item[0]
        date = datetime.fromtimestamp(timestamp_ms / 1000.0).strftime('%Y-%m-%d')
        price = float(item[4])  # Closing price
        grouped_data[date].append(price)

    # Calculate mean price for each day
    mean_prices = []
    for date, prices in grouped_data.items():
        mean_price = sum(prices) / len(prices)
        mean_prices.append({'date': date, 'mean_price': mean_price})

    return mean_prices

# Example usage:
with open('btc_historical_data.json', 'r') as json_file:
    json_data = json.load(json_file)

btc_mean_prices = calculate_mean_price(json_data)

with open('btc_mean_prices.json', 'w') as new_json_file:
    json.dump(btc_mean_prices, new_json_file,indent=1)

print('BTC mean price loading complete')

