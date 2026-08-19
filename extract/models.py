from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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
    market_cap_rank: Optional[int] = None
    fully_diluted_valuation: Optional[float] = None
    total_volume: float

    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    market_cap_change_24h: Optional[float] = None
    market_cap_change_percentage_24h: Optional[float] = None

    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None

    ath: Optional[float] = None
    ath_change_percentage: Optional[float] = None
    ath_date: Optional[datetime] = None

    atl: Optional[float] = None
    atl_change_percentage: Optional[float] = None
    atl_date: Optional[datetime] = None

    roi: Optional[ROI] = None
    last_updated: Optional[datetime] = None