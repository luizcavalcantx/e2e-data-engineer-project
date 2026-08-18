import requests
import json

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "ids": "bitcoin",
    "order": "market_cap_desc",
    "per_page": 1,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
data = response.json()

print(json.dumps(data[0], indent=4))