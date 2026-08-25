with stg as (
    select *
    from {{ref('stg_price_history')}}
),

mart as (
    select
        A.coin_id,
        B.symbol,
        B.first_link as link,
        A.date_timestamp,
        cast(A.date_timestamp as date) as value_date,
        to_char(A.date_timestamp, 'HH24:MI') as value_time,
        round(A.price_value,2) as price_value,
        round(A.market_caps_value,2) as market_caps_value,
        round(A.total_volume_value,2) as total_volume_value,
        current_timestamp() as loaded_at
    from stg as A
    left join {{ref('dim_coin_info')}} as B
        on A.coin_id = B.coin_id
)

select *
from mart