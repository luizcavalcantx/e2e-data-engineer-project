with source as (
    select * from {{ source('raw' , 'coins_markets') }}
),

final as (
    select
        ID as coin_id,
        SYMBOL as symbol,
        NAME as name,
        IMAGE as image,
        CURRENT_PRICE as current_price,
        MARKET_CAP as market_cap,
        MARKET_CAP_RANK as market_cap_rank,
        FULLY_DILUTED_VALUATION as fully_diluted_valuation,
        TOTAL_VOLUME as total_volume,
        HIGH_24H as high_24h,
        LOW_24H as low_24h,
        PRICE_CHANGE_24H as price_change_24h,
        PRICE_CHANGE_PERCENTAGE_24H as price_change_percentage_24h,
        MARKET_CAP_CHANGE_24H as market_cap_change_24h,
        MARKET_CAP_CHANGE_PERCENTAGE_24H as market_cap_change_percentage_24h,
        CIRCULATING_SUPPLY as circulating_supply,
        TOTAL_SUPPLY as total_supply,
        MAX_SUPPLY as max_supply,
        ATH as ath,
        ATH_CHANGE_PERCENTAGE as ath_change_percentage,
        ATH_DATE as ath_date,
        ATL as atl,
        ATL_CHANGE_PERCENTAGE as atl_change_percentage,
        ATL_DATE as atl_date,
        LAST_UPDATED as last_updated,
        current_timestamp() as loaded_at
    from source
)

select * from final