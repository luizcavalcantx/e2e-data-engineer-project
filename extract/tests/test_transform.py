import pandas as pd
from models import CoinMarketData

def test_transform_coins_to_dataframe():
    fake_coins_data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "image": "https://example.com/bitcoin.png",
            "current_price": 68000.0,
            "market_cap": 1300000000000,
            "market_cap_rank": 1,
            "total_volume": 30000000000,
        },
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": "Ethereum",
            "image": "https://example.com/ethereum.png",
            "current_price": 3800.0,
            "market_cap": 450000000000,
            "market_cap_rank": 2,
            "total_volume": 15000000000,
        },
    ]

    coins_list = [CoinMarketData(**coin) for coin in fake_coins_data]
    dict_coins = [coin.model_dump() for coin in coins_list]
    df = pd.DataFrame(dict_coins)

    assert len(df) == 2
    assert list(df["id"]) == ["bitcoin", "ethereum"]
    assert df.loc[df["id"] == "bitcoin", "current_price"].iloc[0] == 68000.0