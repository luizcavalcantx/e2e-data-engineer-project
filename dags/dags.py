import os
from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

aws_credentials = {
    "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
    "AWS_REGION": os.environ.get("AWS_REGION"),
    "S3_BUCKET_NAME": os.environ.get("S3_BUCKET_NAME")
}

extract_env = {**aws_credentials, "COINGECKO_KEY": os.environ["COINGECKO_KEY"]}

with DAG(
    dag_id="crypto_pipeline",
    description="Extrai dados da CoinGecko, carrega no Snowflake e roda transformações dbt",
    start_date=datetime(2026, 8, 27, tzinfo=timezone.utc),
    schedule="@daily",
    catchup=True,
    tags=["crypto", "portfolio"],
) as dag:

    # --- Extração (DockerOperator, imagem crypto-extract) ---
    extract_markets_task = DockerOperator(
        environment=extract_env,
        task_id="extract_markets",
        image="crypto-extract:latest",
        command="extract_markets.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mount_tmp_dir=False,
        retries=3,
        retry_delay=timedelta(seconds=10),
    )

    extract_coin_info_task = DockerOperator(
        environment=extract_env,
        task_id="extract_coin_info",
        image="crypto-extract:latest",
        command="extract_coin_info.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mount_tmp_dir=False,
        retries=3,
        retry_delay=timedelta(seconds=20),
    )

    extract_price_history_task = DockerOperator(
        environment=extract_env,
        task_id="extract_price_history",
        image="crypto-extract:latest",
        command="extract_price_history.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mount_tmp_dir=False,
        retries=3,
        retry_delay=timedelta(seconds=30),
    )

    # --- Carga S3 -> Snowflake RAW (SnowflakeOperator) ---
    load_to_snowflake_task = SQLExecuteQueryOperator(
        task_id="load_to_snowflake",
        conn_id="snowflake_connection",
        sql="""
            copy into raw.coins_markets
                from @crypto_s3_stage
                pattern = '.*coins_markets.*[.]parquet'
                file_format = (type = parquet)
                MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

            copy into raw.coin_info
                from @crypto_s3_stage
                pattern = '.*coins_info.*[.]parquet'
                file_format = (type = parquet)
                MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

            copy into raw.price_history
                from @crypto_s3_stage
                pattern = '.*price_history.*[.]parquet'
                file_format = (type = parquet)
                MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
        """,
    )

    # --- Transformações dbt (DockerOperator, imagem crypto-dbt) ---
    # Mount do profiles.yml: empresta ~/.dbt (do host) para /root/.dbt (dentro do container)
    dbt_profiles_mount = Mount(
        source=os.environ.get("DBT_PROFILES_DIR"),
        target="/root/.dbt",
        type="bind",
    )

    run_dbt_task = DockerOperator(
        task_id="run_dbt",
        image="crypto-dbt:latest",
        command="run",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=[dbt_profiles_mount],
        mount_tmp_dir=False,
    )

    # --- Ordem de execução ---
    # As 3 extrações rodam em paralelo; só depois que as 3 terminarem,
    # a carga no Snowflake roda; e só depois dela, o dbt roda.
    [extract_markets_task, extract_coin_info_task, extract_price_history_task] >> load_to_snowflake_task >> run_dbt_task