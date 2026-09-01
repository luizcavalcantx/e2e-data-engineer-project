# E2E Data Engineer Project

## 📋 Overview
An end-to-end data engineering pipeline that extracts cryptocurrency market data from a public API, lands it in a cloud data lake, transforms it into analytics-ready models, and orchestrates the whole workflow with modern DevOps practices.

## 🏗️ Architecture
CoinGecko API → S3 (raw, date-partitioned Parquet) → Snowflake (RAW → STAGING → MARTS) → dbt → Airflow → Streamlit/Metabase

*(Diagram to be added in `/docs`)*

## 🛠️ Tech Stack
- **Extraction:** Python (`requests`, `pydantic`, `python-dotenv`, `boto3`, `pandas`, `pyarrow`)
- **Raw Storage:** AWS S3 (date-partitioned, Parquet format)
- **Data Warehouse:** Snowflake — `CRYPTO_PIPELINE` database, `RAW` / `STAGING` / `MARTS` schemas, `CRYPTO_PIPELINE_WH` (X-Small, aggressive auto-suspend) warehouse, Storage Integration + External Stage + `COPY INTO`
- **Transformation:** dbt (project: `crypto_pipeline`) — staging & marts layers, tests, documentation, `dbt-labs/dbt_utils`
- **Orchestration:** Apache Airflow 3.3.1 (Docker Compose, `LocalExecutor`), `DockerOperator`-based task execution
- **CI/CD:** GitHub Actions
- **Consumption Layer:** Streamlit / Metabase (TBD)
- **Supporting Tools:** Docker (dedicated Dockerfiles per component), pytest, structured logging, secrets management (`.env`, Docker Compose env substitution)

## 📁 Project Structure
├── extract/ # API extraction scripts (Pydantic models, S3 upload, Dockerfile)

├── dags/ # Airflow DAGs

├── crypto_pipeline/ # dbt project (staging + marts models, Dockerfile)

├── .github/workflows/ # CI/CD pipelines

├── docs/ # Documentation, diagrams, snowflake_setup.sql

└── docker-compose.yml # Airflow stack (postgres, webserver, scheduler — local orchestration)

## 🚀 Project Status
- [x] Repository structure setup
- [x] Data extraction (CoinGecko API, 3 endpoints, 5 coins) — Week 1
  - Pydantic-validated extraction scripts for markets, coin metadata and price history
  - Structured logging, HTTP error handling, reusable S3 upload helper
- [x] AWS S3 raw storage (date-partitioned Parquet)
- [x] Snowflake warehouse setup (Storage Integration, External Stage, RAW tables loaded via `COPY INTO`)
- [x] dbt transformations — Week 2
  - Staging models for markets and price history complete
  - Staging model for coin metadata in progress
  - Marts layer, tests and documentation not started yet
- [x] Containerization & orchestration — Week 3
  - Dockerfiles for extraction and dbt components built
  - Airflow stack (Postgres, webserver, scheduler) running via Docker Compose
  - Airflow connections (AWS, Snowflake) configured
  - Pipeline DAG (`dags/dag.py`) implemented with `DockerOperator` tasks
- [Doing] CI/CD (GitHub Actions)
- [ ] Consumption layer & polish — Week 4

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/luizcavalcantx/e2e-data-engineer-project.git
cd e2e-data-engineer-project/codeup_project
```

### 2. Configure environment variables
Create a `.env` file in the project root with your AWS and Snowflake credentials:
```env
# AWS
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# Snowflake
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database

# Airflow (used by docker-compose / airflow-init)
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin
```

### 3. Set up Python environments (for local development/testing)
```bash
# Extraction
cd extract
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# dbt
cd ../crypto_pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
dbt deps
```

### 4. Configure dbt profile
Make sure `~/.dbt/profiles.yml` exists on your host — it's mounted into the dbt container. Example:
```yaml
crypto_pipeline:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      role: "{{ env_var('DBT_ROLE') }}"
      database: CRYPTO_PIPELINE
      warehouse: CRYPTO_PIPELINE_WH
      schema: STAGING
      threads: 4
```

### 5. Build the pipeline images
```bash
docker build -t crypto-extract:latest ./extract
docker build -t crypto-dbt:latest ./crypto_pipeline
```

### 6. Start the Airflow stack
```bash
docker compose up -d
```
This starts Postgres (Airflow metadata DB), the webserver (`api-server`, port `8080`), and the scheduler. The scheduler bind-mounts `/var/run/docker.sock` so it can spawn the extraction and dbt containers via `DockerOperator`.

### 7. Access the Airflow UI
Go to `http://localhost:8080` and log in with the credentials set in `_AIRFLOW_WWW_USER_USERNAME` / `_AIRFLOW_WWW_USER_PASSWORD`.

### 8. Configure Airflow Connections
In **Admin → Connections**, add:
- `aws_default` — AWS credentials for S3 access
- `snowflake_default` — Snowflake credentials for `COPY INTO` / `SnowflakeOperator` tasks

### 9. Trigger the DAG
Enable and trigger `crypto_pipeline_dag` from the UI, or:
```bash
docker compose exec airflow-scheduler airflow dags trigger crypto_pipeline_dag
```

### 10. Tear down
```bash
docker compose down -v
```
Use `-v` when you need a clean slate (e.g., after changing `.env` values used at `airflow-init` time).

## 📊 Data Source
[CoinGecko API](https://www.coingecko.com/en/api) (free tier, no key required)
- `/coins/markets` → daily market snapshot
- `/coins/{id}` → coin metadata
- `/coins/{id}/market_chart` → historical price data

Tracked coins: Bitcoin, Ethereum, Tether, Solana, Cardano

## 👤 Author
**Luiz Cavalcante**
[LinkedIn](https://www.linkedin.com/in/luizcavalcantx/) · [GitHub](https://github.com/luizcavalcantx)