# E2E Data Engineer Project

## 📋 Overview
An end-to-end data engineering pipeline that extracts cryptocurrency market data from a public API, lands it in a cloud data lake, transforms it into analytics-ready models, and orchestrates the whole workflow with modern DevOps practices.

## 🏗️ Architecture
CoinGecko API → S3 (raw, date-partitioned Parquet) → Snowflake (RAW → STAGING → MARTS) → dbt → Airflow → Streamlit/Metabase

*(Diagram to be added in `/docs`)*

## 🛠️ Tech Stack
- **Extraction:** Python (`requests`, `pydantic`, `python-dotenv`, `boto3`, `pandas`)
- **Raw Storage:** AWS S3 (date-partitioned, Parquet format)
- **Data Warehouse:** Snowflake — `CRYPTO_PIPELINE` database, `RAW` / `STAGING` / `MARTS` schemas, `CRYPTO_PIPELINE_WH` (X-Small) warehouse, external stage + `COPY INTO`
- **Transformation:** dbt (project: `crypto_pipeline`) — staging & marts layers, tests, documentation
- **Orchestration:** Apache Airflow (Docker Compose)
- **CI/CD:** GitHub Actions
- **Consumption Layer:** Streamlit / Metabase
- **Supporting Tools:** Docker, pytest, structured logging, secrets management (`.env`)

## 📁 Project Structure
├── extract/ # API extraction scripts (Pydantic models, S3 upload)

├── dags/ # Airflow DAGs

├── crypto_pipeline/ # dbt project (staging + marts models)

├── .github/workflows/ # CI/CD pipelines

├── docs/ # Documentation, diagrams, snowflake_setup.sql

└── docker-compose.yml # Airflow stack (local orchestration)

## 🚀 Project Status
- [x] Repository structure setup
- [x] Data extraction (CoinGecko API, 3 endpoints, 5 coins) — Week 1
- [x] AWS S3 raw storage (date-partitioned Parquet)
- [x] Snowflake warehouse setup (Storage Integration, External Stage, RAW tables)
- [Doing] dbt transformations (staging models, tests) — Week 2
- [ ] Airflow orchestration + CI/CD — Week 3
- [ ] Consumption layer & polish — Week 4

## ⚙️ How to Run
*(To be completed as the project progresses — setup instructions, environment variables, `docker-compose up`, etc.)*

## 📊 Data Source
[CoinGecko API](https://www.coingecko.com/en/api) (free tier, no key required)
- `/coins/markets` → daily market snapshot
- `/coins/{id}` → coin metadata
- `/coins/{id}/market_chart` → historical price data

Tracked coins: Bitcoin, Ethereum, Tether, Solana, Cardano

## 👤 Author
**Luiz Cavalcante**
[LinkedIn](https://www.linkedin.com/in/luizcavalcantx/) · [GitHub](https://github.com/luizcavalcantx)