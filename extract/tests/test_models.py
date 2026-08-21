import pytest
from pydantic import ValidationError
from models import CoinMarketData

def test_coin_market_data_valid():
    fake_api_response = {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "image": "https://example.com/bitcoin.png",
        "current_price": 68000.0,
        "market_cap": 1300000000000,
        "market_cap_rank": 1,
        "total_volume": 30000000000,
        "high_24h": 69000.0,
        "low_24h": 67000.0,
        "circulating_supply": 19000000,
        "ath": 73000.0,
        "ath_date": "2024-03-14T07:10:36.635Z",
        "atl": 67.81,
        "atl_date": "2013-07-06T00:00:00.000Z",
        "roi": None,
        "last_updated": "2024-04-07T16:49:31.736Z"
    }

    coin = CoinMarketData(**fake_api_response)

    assert coin.id == "bitcoin"
    assert coin.name == "Bitcoin"
    assert coin.current_price == 68000.0


def test_coin_market_data_missing_required_field():
    incomplete_response = {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        # faltando: "image", "current_price", "market_cap", "total_volume"
    }

    with pytest.raises(ValidationError):
        CoinMarketData(**incomplete_response)