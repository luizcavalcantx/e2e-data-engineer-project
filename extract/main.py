import requests
import json
from models import CoinMarketData
import pandas as pd
from datetime import date

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,tether,ripple,binancecoin,solana,usd-coin,dogecoin,cardano,tron",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
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
df.to_parquet(f"extract/tmp/coins_parquet_{date.today()}.parquet", index=False)