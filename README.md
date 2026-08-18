# E2E Data Engineer Project

## 📋 Overview
An end-to-end data engineering pipeline that extracts data from a public API, lands it in a cloud data lake, transforms it into analytics-ready models, and orchestrates the whole workflow with modern DevOps practices.

## 🏗️ Architecture
API → S3 (raw, partitioned by date) → Snowflake → dbt → Airflow → Streamlit/Metabase

*(Diagram to be added in `/docs`)*

## 🛠️ Tech Stack
- **Extraction:** Python (`requests`, `pydantic`, `python-dotenv`, `boto3`)
- **Raw Storage:** AWS S3 (date-partitioned, Parquet format)
- **Data Warehouse:** Snowflake (external stage + `COPY INTO`)
- **Transformation:** dbt (staging & marts layers, tests, documentation)
- **Orchestration:** Apache Airflow (Docker Compose)
- **CI/CD:** GitHub Actions
- **Consumption Layer:** Streamlit / Metabase
- **Supporting Tools:** Docker, pytest, logging, secrets management

## 📁 Project Structure
├── extract/ # API extraction scripts

├── dags/ # Airflow DAGs

├── dbt_project/ # dbt models (staging + marts)

├── .github/workflows/ # CI/CD pipelines

├── docs/ # Documentation and diagrams

└── docker-compose.yml # Airflow stack (local orchestration)

## 🚀 Project Status
- [x] Repository structure setup
- [ ] Data extraction (Week 1)
- [ ] dbt transformations (Week 2)
- [ ] Airflow orchestration + CI/CD (Week 3)
- [ ] Consumption layer & polish (Week 4)

## ⚙️ How to Run
*(To be completed as the project progresses — setup instructions, environment variables, `docker-compose up`, etc.)*

## 📊 Data Source
*(To be defined — public API selection in progress)*

## 👤 Author
**Luiz Cavalcante**
[LinkedIn](https://www.linkedin.com/in/luizgustavocavalcantes/) · [GitHub](https://github.com/luizcavalcantx)