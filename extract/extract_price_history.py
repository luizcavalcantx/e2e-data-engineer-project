import requests
import json
from models import PriceHistoryData
import pandas as pd
from datetime import date
import time

coin_ids = ['bitcoin','ethereum','tether','solana','cardano']
base_url = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

coins_info = []
for coin_id in coin_ids:
    url = base_url.format(id=coin_id)
    params = {
        "vs_currency": "usd",
        "days": "365",
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    coin = PriceHistoryData(**response.json())
    coin_dict = coin.model_dump()
    coin_dict["coin_id"] = coin_id
    coins_info.append(coin_dict)
    time.sleep(6)

print(coins_info)

df = pd.DataFrame(coins_info)
df.to_parquet(f"extract/tmp/price_history_{date.today()}.parquet", index=False)

print(df.columns.tolist())
print(df.head())