import requests
from datetime import datetime, timezone
import csv
import os
import pandas as pd

def get_latest_block_height():
    url = "https://mempool.space/api/v1/blocks"
    response = requests.get(url)
    if response.status_code == 200:
        blocks = response.json()
        return blocks[0]["height"]
    else:
        print("Failed to fetch the latest block height.")
        return None

def fetch_block_data(block_height):
    url = f"https://mempool.space/api/v1/blocks/{block_height}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        blocks = response.json()
        
        block_data = []
        for block in blocks:
            timestamp = block.get("timestamp")
            if timestamp:
                date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M')
            else:
                date = None
            
            block_info = {
                "date": date,
                "medianFee": block.get("extras", {}).get("medianFee"),
                "avgFeeRate": block.get("extras", {}).get("avgFeeRate")
            }
            block_data.append(block_info)
        
        return block_data
    else:
        return f"Failed to retrieve data: {response.status_code}"

def append_to_csv_file(data, filename):
    fieldnames = ["date", "medianFee", "avgFeeRate"]
    file_exists = os.path.exists(filename)
    with open(filename, 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for block in data:
            writer.writerow(block)



start_block = 400000
latest_block_height = get_latest_block_height()

if latest_block_height:
    block_height = start_block
    print(fetch_block_data(start_block))
    for block_height in range(start_block, latest_block_height + 1, 15):
        print(block_height)
        block_data = fetch_block_data(block_height)
        if block_data:
            append_to_csv_file(block_data, 'block_data.csv')
            print(block_data)   
        else:
            print(f"Failed to retrieve data for block {block_height}")

