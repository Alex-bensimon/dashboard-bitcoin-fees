import requests
from datetime import datetime, timezone
import pandas as pd
import pandas_gbq
from pandas_gbq import to_gbq


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
            # Convert timestamp to human-readable date
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
        # Return an error message if the request was not successful
        return f"Failed to retrieve data: {response.status_code}"
    
def filter_data(data):
    current_date = datetime.now().strftime("%Y-%m-%d")
    filtered_data = [data_point for data_point in data if data_point['date'].startswith(current_date)]
    return filtered_data

def create_df(data):
    transformed_data = []
    for data_point in data:
        transformed_data.append({
            'date': datetime.strptime(data_point['date'], '%Y-%m-%d %H:%M'),  
            'avgFeeRate': round(data_point['avgFeeRate'], 3),
            'medianFee': round(data_point['medianFee'], 3)
        })
    df = pd.DataFrame(transformed_data)
    return df


def main():
    # Get the latest block height
    latest_block_height = get_latest_block_height()
    if latest_block_height is not None:
        print(f"Latest block height: {latest_block_height}")
        block_data = fetch_block_data(latest_block_height)
        filtered_block_data = filter_data(block_data)
        if isinstance(filtered_block_data, list):
            print("Fetched block data successfully.")
            df = create_df(filtered_block_data)
            dest_table = "bitcoin_fees.bitcoin-24h-fees"
            project_id = "dashboard-bitcoin-fees"
            pandas_gbq.to_gbq(df,dest_table,project_id=project_id,if_exists='append')
            print(df)
        else:
            print(block_data)
    else:
        print("Could not fetch the latest block height.")

