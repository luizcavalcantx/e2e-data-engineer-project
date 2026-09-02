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

def fetch_market_data():
    """Call the coingecko markets endpoint and returns raw json data"""
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def validate_and_transform(raw_data):
    """Validates raw API data against the Pydantic model and returns a DataFrame."""
    coins = [CoinMarketData(**coin) for coin in raw_data]
    dict_coins = [coin.model_dump() for coin in coins]
    return pd.DataFrame(dict_coins)

def save_to_parquet(df,today):
    """Saves the DataFrame locally as Parquet and returns the local path"""
    os.makedirs("tmp", exist_ok=True)
    local_path = f"tmp/coins_parquet_{today}.parquet"
    df.to_parquet(local_path, index=False)
    return local_path

def build_s3_key(today):
    return f"raw/coins_markets/dt={today}/coins_parquet_{today}.parquet"

def run():
    logger.info("Starting extraction")

    raw_data = fetch_market_data()
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