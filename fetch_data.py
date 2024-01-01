from datetime import datetime
import time
import requests
import pandas as pd

def fetch_data(symbol, category, interval):
    url = "https://api.bybit.com/v5/market/kline"
    timestamp = int(time.time())
    values = []

    while True:
        params = {
            "symbol": symbol,
            "interval": interval,
            "category": category,
            "start": (timestamp - 200 * 60 * interval) * 1000,
            "end": timestamp * 1000,
            "limit": 200
        }

        response = requests.get(url, params=params)
        response_data = response.json()

        if len(response_data["result"]["list"]) == 0:
            break

        values += response_data["result"]["list"]
        timestamp -= 200 * 60 * interval

    data = pd.DataFrame(values)
    data.columns = ["timestamp", "open", "high", "low", "close", "volume", "turnover"]
    data["datetime"] = (data['timestamp'].astype(int)/1000).apply(datetime.fromtimestamp)
    data.sort_values("datetime", inplace=True)
    data.set_index("datetime", inplace=True)

    return data

# Example usage:
symbol = "BTCUSDT"
category = "linear"
interval = 15

result_data = fetch_data(symbol, category, interval)
print(result_data)
