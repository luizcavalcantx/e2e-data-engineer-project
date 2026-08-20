import requests
import json
from models import CoinInfoData
import pandas as pd
from datetime import date
import time

coin_ids = ['bitcoin','ethereum','tether','solana','cardano']
base_url = "https://api.coingecko.com/api/v3/coins/{id}"

coins_info = []
for coin_id in coin_ids:
    url = base_url.format(id=coin_id)
    params = {
        "localization": False,
        "tickers": False,
        "market_data": False,
        "community_data": False,
        "developer_data": False,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    coin = CoinInfoData(**response.json())
    coins_info.append(coin.model_dump())
    time.sleep(6) # to rate limit of free coingecko API

print(coins_info)

df = pd.DataFrame(coins_info)
df.to_parquet(f"extract/tmp/coins_info_{date.today()}.parquet", index=False)