import os
import requests
import json
from models import CoinMarketData
import pandas as pd
from datetime import date
from upload_s3 import upload_to_s3
from logger_config import setup_logger

logger = setup_logger("extract_markets")

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,tether,solana,cardano",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False
}

logger.info("Starting extraction")

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

coins_list = []
for coin_data in data:
    coin = CoinMarketData(**coin_data)
    coins_list.append(coin)

## Transforming into a dictionay list again
# or: dict_coin = [coin.model() for coin in coins_list]
dict_coins = []
for coin_dict in coins_list:
    x = coin_dict.model_dump()
    dict_coins.append(x)

df = pd.DataFrame(dict_coins)
logger.info(f"Sucessfully fetched data for {len(data)} coins")

os.makedirs("tmp", exist_ok=True)

local_path = f"tmp/coins_parquet_{date.today()}.parquet"
df.to_parquet(local_path, index=False)

s3_key = f"raw/coins_markets/dt={date.today()}/coins_parquet_{date.today()}.parquet"

try:
    upload_to_s3(local_path, s3_key)
    logger.info(f"Successfully upload to S3: {s3_key}")
    os.remove(local_path)
    logger.info(f"Removed local file: {local_path}")
except Exception as e:
    logger.error(f"Failed to upload to S3: {e}")