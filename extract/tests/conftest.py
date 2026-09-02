import sys
import os
import pytest

# Adds the extract/ folder (one level up from tests/) to sys.path so that
# test modules can import extract_markets, extract_coin_info, etc. directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def sample_market_response():
    """Minimal valid CoinGecko /coins/markets response for one coin."""
    return [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "image": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png",
            "current_price": 65000.0,
            "market_cap": 1280000000000,
            "market_cap_rank": 1,
            "total_volume": 25000000000,
            "price_change_percentage_24h": 1.5,
            "circulating_supply": 19700000.0,
            "last_updated": "2026-08-19T00:00:00.000Z",
        }
    ]


@pytest.fixture
def sample_coin_info_response():
    """Minimal valid CoinGecko /coins/{id} response for one coin."""
    return {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "categories": ["Cryptocurrency", "Layer 1"],
        "links": {
            "homepage": ["https://bitcoin.org"],
            "blockchain_site": ["https://blockchair.com/bitcoin"],
            "official_forum_url": ["https://bitcointalk.org"],
            "subreddit_url": "https://reddit.com/r/bitcoin",
        },
        "image": {
            "thumb": "https://coin-images.coingecko.com/coins/images/1/thumb/bitcoin.png",
            "small": "https://coin-images.coingecko.com/coins/images/1/small/bitcoin.png",
            "large": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png",
        },
        "country_origin": None,
        "genesis_date": "2009-01-03",
        "market_cap_rank": 1,
    }


@pytest.fixture
def sample_price_history_response():
    """Minimal valid CoinGecko /coins/{id}/market_chart response for one coin."""
    return {
        "prices": [[1755561600000, 65000.0], [1755648000000, 65200.0]],
        "market_caps": [[1755561600000, 1280000000000], [1755648000000, 1285000000000]],
        "total_volumes": [[1755561600000, 25000000000], [1755648000000, 25100000000]],
    }