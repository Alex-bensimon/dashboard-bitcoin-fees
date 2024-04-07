import requests
import json
import pandas as pd
from datetime import datetime

import requests

def get_btc_fee():
    url = 'https://api.blockchain.info/mempool/fees'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Failed to fetch data: Status code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    btc_fee = get_btc_fee()
    print(btc_fee)

