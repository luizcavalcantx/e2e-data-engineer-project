import requests
import json
from models import PriceHistoryData
import pandas as pd
from datetime import date
import time
from upload_s3 import upload_to_s3

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

df = pd.DataFrame(coins_info)
local_path = f"extract/tmp/price_history_{date.today()}.parquet"
df.to_parquet(local_path, index=False)

s3_key = f"raw/price_history/price_history_{date.today()}.parquet"
upload_to_s3(local_path, s3_key)