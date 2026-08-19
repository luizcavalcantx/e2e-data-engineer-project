import requests
import json
from models import CoinMarketData

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

lista_coins = []
for coin_data in data:
    coin = CoinMarketData(**coin_data)
    lista_coins.append(coin)

for coin in lista_coins:
    print(f"{coin.name} ({coin.symbol.upper()}): ${coin.current_price}")