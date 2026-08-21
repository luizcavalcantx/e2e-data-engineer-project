import requests
import json
from models import CoinInfoData
import pandas as pd
from datetime import date
import time
from upload_s3 import upload_to_s3
from logger_config import setup_logger

logger = setup_logger("extract_coin_info")

coin_ids = ['bitcoin','ethereum','tether','solana','cardano']
base_url = "https://api.coingecko.com/api/v3/coins/{id}"

logger.info("Starting extraction")
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

df = pd.DataFrame(coins_info)
logger.info(f"Successfully fetched data for {len(df)} coins")

local_path = f"extract/tmp/coins_info_{date.today()}.parquet"
df.to_parquet(local_path, index=False)

s3_key = f"raw/coins_info/dt={date.today()}/coins_info_{date.today()}.parquet"

try:
    upload_to_s3(local_path, s3_key)
    logger.info(f"Successfully upload to S3: {s3_key}")
except Exception as e:
    logger.error(f"Failed to upload to S3: {e}")