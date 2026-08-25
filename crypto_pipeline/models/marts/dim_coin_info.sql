with stg as (
    select *
    from {{ref('stg_coin_info')}}
),

mart as (
select
    coin_id,
    symbol,
    name,
    categories[0]::STRING as first_category,
    links:homepage[0]::STRING as first_link,
    creation_date,
    loaded_at
from stg)

select *
from mart