with stg as (
    select *
    from {{ref('stg_coins_markets')}}
),

mart as (
    select
        A.coin_id,
        A.symbol,
        A.name,
        B.first_link as link,
        A.image,
        round(A.current_price,2) as current_price,
        A.market_cap,
        A.market_cap_rank,
        A.fully_diluted_valuation,
        A.total_volume,
        round(A.high_24h,2) as high_24h,
        round(A.low_24h,2) as low_24h,
        A.price_change_24h,
        A.price_change_percentage_24h,
        A.market_cap_change_24h,
        A.market_cap_change_percentage_24h,
        A.circulating_supply,
        A.total_supply,
        A.max_supply,
        A.ath,
        A.ath_change_percentage,
        A.ath_date,
        A.atl,
        A.atl_change_percentage,
        A.atl_date,
        A.last_updated,
        current_timestamp() as loaded_at
    from stg as A
    left join {{ref('dim_coin_info')}} as B
        on A.coin_id = B.coin_id
)

select *
from mart