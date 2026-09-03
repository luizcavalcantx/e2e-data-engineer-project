from datetime import datetime

from pydantic import BaseModel


class ROI(BaseModel):
    times: float
    currency: str
    percentage: float


class CoinMarketData(BaseModel):
    id: str
    symbol: str
    name: str
    image: str

    current_price: float
    market_cap: float
    market_cap_rank: int | None = None
    fully_diluted_valuation: float | None = None
    total_volume: float

    high_24h: float | None = None
    low_24h: float | None = None
    price_change_24h: float | None = None
    price_change_percentage_24h: float | None = None
    market_cap_change_24h: float | None = None
    market_cap_change_percentage_24h: float | None = None

    circulating_supply: float | None = None
    total_supply: float | None = None
    max_supply: float | None = None

    ath: float | None = None
    ath_change_percentage: float | None = None
    ath_date: datetime | None = None

    atl: float | None = None
    atl_change_percentage: float | None = None
    atl_date: datetime | None = None

    roi: ROI | None = None
    last_updated: datetime | None = None

class CoinLinks(BaseModel):
    homepage: list[str]
    blockchain_site: list[str]
    official_forum_url: list[str]
    subreddit_url: str | None = None


class CoinImage(BaseModel):
    thumb: str | None = None
    small: str | None = None
    large: str | None = None


class CoinInfoData(BaseModel):
    id: str
    symbol: str
    name: str
    categories: list[str | None] = []
    links: CoinLinks
    image: CoinImage
    country_origin: str | None = None
    genesis_date: str | None = None
    market_cap_rank: int | None = None

class PriceHistoryData(BaseModel):
    prices: list[list[float]]
    market_caps: list[list[float]]
    total_volumes: list[list[float]]