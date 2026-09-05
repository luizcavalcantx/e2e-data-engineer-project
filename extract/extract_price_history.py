import os
import time
from datetime import date

import pandas as pd
import requests

from logger_config import setup_logger
from models import PriceHistoryData
from upload_s3 import upload_to_s3
from dotenv import load_dotenv

api_key = os.environ["COINGECKO_KEY"]

logger = setup_logger("extract_price_history")

coin_ids = ["bitcoin", "ethereum", "tether", "solana", "cardano"]
base_url = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"
headers = {"x-cg-demo-api-key": api_key}
params = {
    "vs_currency": "usd",
    "days": "365",
    "interval": "daily",
}

def fetch_price_history():
    """Call the coingecko market_chart endpoint for each coin and returns raw json data"""
    raw_data = []
    for coin_id in coin_ids:
        url = base_url.format(id=coin_id)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        raw_data.append((coin_id, response.json()))
        # time.sleep(6)  # respect the free coingecko API rate limit
    return raw_data

def validate_and_transform(data):
    """Validates raw API data against the Pydantic model and returns a DataFrame."""
    coins_list = []
    for coin_id, coin_data in data:
        coin = PriceHistoryData(**coin_data)
        coins_list.append((coin_id, coin))

    dict_coins = []
    for coin_id, coin_dict in coins_list:
        x = coin_dict.model_dump()
        x["coin_id"] = coin_id
        dict_coins.append(x)

    return pd.DataFrame(dict_coins)

def save_to_parquet(df, today):
    """Saves the DataFrame locally as Parquet and returns the local path"""
    os.makedirs("tmp", exist_ok=True)
    local_path = f"tmp/price_history_{today}.parquet"
    df.to_parquet(local_path, index=False)
    return local_path

def build_s3_key(today):
    return f"raw/price_history/dt={today}/price_history_{today}.parquet"

def run():
    logger.info("Starting extraction")
    # time.sleep(30)

    raw_data = fetch_price_history()
    df = validate_and_transform(raw_data)
    logger.info(f"Successfully fetched data for {len(df)} coins")

    today = date.today()
    local_path = save_to_parquet(df, today)
    s3_key = build_s3_key(today)

    try:
        upload_to_s3(local_path, s3_key)
        logger.info(f"Successfully upload to S3: {s3_key}")
        os.remove(local_path)
        logger.info(f"Removed local file: {local_path}")
    except Exception as e:
        logger.error(f"Failed to upload to S3: {e}")
        raise

if __name__ == "__main__":
    run()