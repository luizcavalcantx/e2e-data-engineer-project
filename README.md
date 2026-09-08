# E2E Data Engineer Project

## 📋 Overview
An end-to-end data engineering pipeline that extracts cryptocurrency market data from a public API, lands it in a cloud data lake, transforms it into analytics-ready models, and orchestrates the whole workflow with modern DevOps practices.

## 🏗️ Architecture
CoinGecko API → S3 (raw, date-partitioned Parquet) → Snowflake (RAW → STAGING → MARTS) → dbt → Airflow → Streamlit/Metabase

## 🛠️ Tech Stack
- **Extraction:** Python (`requests`, `pydantic`, `python-dotenv`, `boto3`, `pandas`, `pyarrow`) — CoinGecko demo API key sent via the `x-cg-demo-api-key` header (`COINGECKO_KEY`) to raise the rate limit and drop `time.sleep` throttling
- **Testing:** `pytest`, `pytest-mock` — unit tests for all extraction scripts (fetch, validation, transformation, Parquet save, S3 key generation), with external calls (`requests`, `boto3`) mocked
- **Raw Storage:** AWS S3 (date-partitioned, Parquet format)
- **Data Warehouse:** Snowflake — `CRYPTO_PIPELINE` database, `RAW` / `STAGING` / `MARTS` schemas, `CRYPTO_PIPELINE_WH` (X-Small, aggressive auto-suspend) warehouse, Storage Integration + External Stage + `COPY INTO`
- **Transformation:** dbt (project: `crypto_pipeline`) — staging & marts layers, tests, documentation, `dbt-labs/dbt_utils`
- **Orchestration:** Apache Airflow 3.3.1 (Docker Compose, `LocalExecutor`), `DockerOperator`-based task execution
- **CI/CD:** GitHub Actions — lint (`ruff`), `pytest` and `dbt build` running on every push/PR
- **Consumption Layer:** Streamlit / Metabase (TBD)
- **Supporting Tools:** Docker (dedicated Dockerfiles per component), structured logging, secrets management (`.env`, Docker Compose env substitution)
- **Python environments:** two isolated virtualenvs, one per deployable component — `extract/.venv` (extraction + tests, mirrors `crypto-extract:latest`) and `crypto_pipeline/.venv` (dbt, mirrors `crypto-dbt:latest`). They are kept separate on purpose: dbt's dependency tree (`dbt-core`, `dbt-snowflake`, `metricflow`, pinned `Jinja2`/`protobuf`/`click`) is large and would bloat or conflict with the lean extraction runtime. Each `.venv` sits next to the `requirements.txt` and `Dockerfile` it matches, and next to the CI `working-directory`.

## 🔄 Data Pipeline

### Raw Layer (S3)
- **Frequency:** Daily
- **Source:** CoinGecko API (`/coins/markets`, `/coins/{id}`, `/coins/{id}/market_chart`)
- **Storage:** S3, Parquet format, partitioned by date (`dt=YYYY-MM-DD/`)

### RAW Layer (Snowflake)
- **Source:** S3, via Storage Integration + External Stage
- **Process:** `COPY INTO` raw tables
- **Schema:** `RAW`

### STAGING Layer (dbt)
- **Process:** dbt staging models — data cleaning, type casting, validation
- **Models:** `stg_coins_markets`, `stg_coin_info`, `stg_price_history`
- **Status:** complete
- **Schema:** `STAGING`

### MARTS Layer (dbt)
- **Process:** business logic and analytics-ready models
- **Models:** `dim_coin_info` (coin dimension), `fct_daily_market_snapshot` (daily market state per coin), `fct_price_history` (historical daily prices)
- **Status:** models, descriptions and tests in place (`not_null` / `unique` keys, `dbt_utils.unique_combination_of_columns`)
- **Schema:** `MARTS`

## 📊 Current Capacity

> Note: these numbers reflect the current development environment, where the pipeline has been run periodically during testing rather than on a continuous production schedule.

| Metric | Value |
|---|---|
| Cryptocurrencies tracked | 5 (bitcoin, ethereum, tether, solana, cardano) |
| API endpoints | 3 (coins/markets, coin_info, price_history) |
| Total objects in S3 | 10 |
| Total storage | ~306 KB (Parquet, compressed) |
| Storage per endpoint | coins_markets: ~53 KB · coins_info: ~42 KB · price_history: ~211 KB |
| Partitioning | Date-based (`dt=YYYY-MM-DD/`) per endpoint |
| File format | Apache Parquet (columnar, schema-preserving) |

## 📁 Project Structure
├── extract/ # API extraction scripts (Pydantic models, S3 upload, Dockerfile, pytest suite, .venv)

├── dags/ # Airflow DAGs (dags.py — dag_id: crypto_pipeline)

├── crypto_pipeline/ # dbt project (staging + marts models, Dockerfile, .venv)

├── notebooks/ # Exploratory notebooks / API studies (not part of the pipeline)

├── .github/workflows/ # CI/CD pipelines (lint, pytest, dbt build)

├── docs/ # Documentation, diagrams, snowflake_setup.sql / grants_setup.sql / create_airflow.sql

└── docker-compose.yml # Airflow stack (postgres, webserver, scheduler, dag-processor — local orchestration)

## 🚀 Project Status
- [x] Repository structure setup
- [x] Data extraction (CoinGecko API, 3 endpoints, 5 coins) — Week 1
  - Pydantic-validated extraction scripts for markets, coin metadata and price history
  - Structured logging, HTTP error handling, reusable S3 upload helper
  - All extraction scripts refactored into pure, testable functions (`fetch`, `validate_and_transform`, `save_to_parquet`, `build_s3_key`, `run`)
- [x] AWS S3 raw storage (date-partitioned Parquet)
- [x] Snowflake warehouse setup (Storage Integration, External Stage, RAW tables loaded via `COPY INTO`)
- [x] dbt transformations — Week 2
  - Staging models complete for all three sources (`stg_coins_markets`, `stg_coin_info`, `stg_price_history`)
  - Marts layer built: `dim_coin_info`, `fct_daily_market_snapshot`, `fct_price_history` — with column descriptions and schema tests
  - `dbt-labs/dbt_utils` in use for cross-column uniqueness tests
- [x] Containerization & orchestration — Week 3
  - Dockerfiles for extraction and dbt components built
  - Airflow stack (Postgres, webserver, scheduler, dag-processor) running via Docker Compose
  - Snowflake Airflow connection configured; AWS + CoinGecko creds passed to containers via env
  - Pipeline DAG (`dags/dags.py`, `dag_id="crypto_pipeline"`) implemented with `DockerOperator` tasks — 3 extractions in parallel → `load_to_snowflake` → `run_dbt`
- [x] CI/CD (GitHub Actions) — Week 4
  - Unit test suite (`pytest` + `pytest-mock`) covering all three extraction scripts and the S3 upload helper
  - Lint step (`ruff`) running in CI
  - `pytest` step running in CI
  - `dbt build` step running in CI

## 🧪 Testing
The `extract/` module has a full unit test suite under `extract/tests/`:

- `test_extract_markets.py`, `test_extract_coin_info.py`, `test_extract_price_history.py` — cover API fetching, Pydantic validation (valid and malformed data), DataFrame transformation, local Parquet save, and S3 key generation for each extraction script
- `test_upload_s3.py` — verifies the S3 upload helper calls `boto3` with the correct parameters
- `conftest.py` — adds `extract/` to `sys.path` and holds shared fixtures with sample CoinGecko API responses for each of the three endpoints
- All external I/O (`requests.get`, `boto3` client) is mocked, so the suite runs fast and without hitting the real API or AWS

Run locally from `extract/` (with `extract/.venv` active):
```bash
pip install pytest pytest-mock
pytest -v
```

In CI the pytest step sets a dummy `COINGECKO_KEY` so the extraction modules import cleanly without a real key.

## 🔄 CI/CD
Every push and pull request runs a GitHub Actions workflow (`.github/workflows/ci.yml`) with three stages:

1. **Lint** — `ruff` checks the codebase for style and correctness issues.
2. **Test** — the `pytest` suite runs against the `extract/` module, with all external calls mocked.
3. **dbt build** — the `crypto_pipeline` dbt project is compiled and run against Snowflake to catch modeling or dependency errors before merge.

A failure in any stage blocks the workflow, so broken code or models don't reach `main`.

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/luizcavalcantx/e2e-data-engineer-project.git
cd e2e-data-engineer-project/codeup_project
```

### 2. Configure environment variables
Create a `.env` file in the project root (it is git-ignored). Docker Compose substitutes these into the Airflow services, and the extraction containers receive the AWS + CoinGecko values through the DAG:
```env
# AWS (S3 raw storage)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# CoinGecko (demo API key — sent as x-cg-demo-api-key header)
COINGECKO_KEY=CG-xxxxxxxxxxxxxxxxxxxx

# Airflow metadata DB (Postgres)
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

# Airflow admin user (created by airflow-init) + core secrets
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=admin
AIRFLOW_ADMIN_FIRSTNAME=Admin
AIRFLOW_ADMIN_LASTNAME=User
AIRFLOW_ADMIN_EMAIL=admin@example.com
AIRFLOW_JWT_SECRET=generate_a_random_string
AIRFLOW_FERNET_KEY=generate_with_python_cryptography_fernet

# dbt profiles dir on the host (bind-mounted into the dbt container)
DBT_PROFILES_DIR=/absolute/path/to/your/.dbt
```
Generate the Fernet key with:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Set up Python environments (for local development/testing)
Two separate virtualenvs, one per component (see **Tech Stack → Python environments** for the rationale). Activate the one that matches the folder you're working in.
```bash
# Extraction  (extract/.venv  ->  crypto-extract image)
cd extract
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-mock  # dev/test dependencies

# dbt  (crypto_pipeline/.venv  ->  crypto-dbt image)
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
This starts Postgres (Airflow metadata DB), the webserver (`api-server`, port `8080`), the scheduler and the dag-processor. The scheduler bind-mounts `/var/run/docker.sock` so it can spawn the extraction and dbt containers via `DockerOperator`, and `${DBT_PROFILES_DIR}` into `~/.dbt`.

### 7. Access the Airflow UI
Go to `http://localhost:8080` and log in with the credentials set in `AIRFLOW_ADMIN_USER` / `AIRFLOW_ADMIN_PASSWORD`.

### 8. Configure Airflow Connections
In **Admin → Connections**, add:
- `snowflake_connection` — Snowflake credentials for the `load_to_snowflake` task (`COPY INTO` from the external stage)

AWS and CoinGecko credentials are **not** Airflow connections — they are passed straight into the extraction containers as environment variables by the DAG (`extract_env` in `dags/dags.py`), sourced from the scheduler's environment.

### 9. Trigger the DAG
Enable and trigger `crypto_pipeline` from the UI, or:
```bash
docker compose exec airflow-scheduler airflow dags trigger crypto_pipeline
```

### 10. Tear down
```bash
docker compose down -v
```
Use `-v` when you need a clean slate (e.g., after changing `.env` values used at `airflow-init` time).

## 📊 Data Source
[CoinGecko API](https://www.coingecko.com/en/api) (free "Demo" plan — a personal API key is sent via the `x-cg-demo-api-key` header to lift the anonymous rate limit)
- `/coins/markets` → daily market snapshot
- `/coins/{id}` → coin metadata
- `/coins/{id}/market_chart` → historical price data

Tracked coins: Bitcoin, Ethereum, Tether, Solana, Cardano

## 👤 Author
**Luiz Cavalcante**
[LinkedIn](https://www.linkedin.com/in/luizcavalcantx/) · [GitHub](https://github.com/luizcavalcantx)