import os
from datetime import date

import pandas as pd
import requests

from logger_config import setup_logger
from models import CoinInfoData
from upload_s3 import upload_to_s3

api_key = os.environ["COINGECKO_KEY"]

logger = setup_logger("extract_coin_info")

coin_ids = ["bitcoin", "ethereum", "tether", "solana", "cardano"]
base_url = "https://api.coingecko.com/api/v3/coins/{id}"
headers = {"x-cg-demo-api-key": api_key}
params = {
    "localization": False,
    "tickers": False,
    "market_data": False,
    "community_data": False,
    "developer_data": False,
    "sparkline": False
}

def fetch_coin_info():
    """Call the coingecko coins/{id} endpoint for each coin and returns raw json data"""
    raw_data = []
    for coin_id in coin_ids:
        url = base_url.format(id=coin_id)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        raw_data.append(response.json())
    return raw_data

def validate_and_transform(data):
    """Validates raw API data against the Pydantic model and returns a DataFrame."""
    coins_list = []
    for coin_data in data:
        coin = CoinInfoData(**coin_data)
        coins_list.append(coin)

    dict_coins = []
    for coin_dict in coins_list:
        x = coin_dict.model_dump()
        dict_coins.append(x)

    return pd.DataFrame(dict_coins)

def save_to_parquet(df, today):
    """Saves the DataFrame locally as Parquet and returns the local path"""
    os.makedirs("tmp", exist_ok=True)
    local_path = f"tmp/coins_info_{today}.parquet"
    df.to_parquet(local_path, index=False)
    return local_path

def build_s3_key(today):
    return f"raw/coins_info/dt={today}/coins_info_{today}.parquet"

def run():
    logger.info("Starting extraction")

    raw_data = fetch_coin_info()
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
