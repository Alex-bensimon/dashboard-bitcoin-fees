import requests
import json
from datetime import datetime, timedelta

def get_binance_data_for_specific_day(symbol, interval, specific_day):
    start_time = datetime.combine(specific_day, datetime.min.time())  # Start at 00:00 of the specific day
    end_time = start_time + timedelta(days=1)  # End just before 00:00 of the next day
    
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=1000"
    url += f"&startTime={int(start_time.timestamp() * 1000)}"
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
specific_day = datetime.now()  # Specific day for historical data

btc_data_for_day = get_binance_data_for_specific_day(symbol, interval, specific_day)

if btc_data_for_day:
    # Optionally, convert the data to a more readable format or directly work with it as needed
    print("BTC data for the specified day:", btc_data_for_day)
else:
    print("No data found for the specified day.")

# Depending on your needs, you can further process this data,
# such as saving it to a JSON file or performing calculations.
