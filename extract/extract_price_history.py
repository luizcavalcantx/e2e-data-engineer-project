import requests
import json
from models import PriceHistoryData
import pandas as pd
from datetime import date
import time
from upload_s3 import upload_to_s3
from logger_config import setup_logger

logger = setup_logger("extract_price_history")

coin_ids = ['bitcoin','ethereum','tether','solana','cardano']
base_url = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

logger.info("Starting extraction")
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
logger.info(f"Successfully fetched data for {len(df)} coins")

local_path = f"extract/tmp/price_history_{date.today()}.parquet"
df.to_parquet(local_path, index=False)

s3_key = f"raw/price_history/price_history_{date.today()}.parquet"

try:
    upload_to_s3(local_path, s3_key)
    logger.info(f"Successfully upload to S3: {s3_key}")
except Exception as e:
    logger.error(f"Failed to upload to S3: {e}")