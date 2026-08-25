### Architectural Diagram

┌────────────────┐
│ Open-Meteo │
│ REST API │
└───────┬────────┘
│ (HTTP GET - Hourly Weather JSON)
▼
┌────────────────────────────────────────────────────────┐
│ Extraction & Ingestion │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Python OOP Extractor (Prefect Task) │ │
│ │ - Retries, Backoff, Schema Validation (Pydantic)│ │
│ └────────────────────────┬─────────────────────────┘ │
└───────────────────────────┼────────────────────────────┘
│
▼ (Raw GCS Upload)
┌────────────────────────────────────────────────────────┐
│ Google Cloud Storage (Data Lake) │
│ gs://weather-lake-raw/year=YYYY/month=MM/day=DD/ │
└───────────────────────────┬────────────────────────────┘
│
▼ (GCS-to-BigQuery Load Task)
┌────────────────────────────────────────────────────────┐
│ Google BigQuery (Lakehouse) │
│ │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Bronze Layer: raw_layer.raw_weather (JSON string)│ │
│ └────────────────────────┬─────────────────────────┘ │
│ │ │
│ ▼ (dbt transformations) │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Silver Layer: stg_actuals & stg_forecasts │ │
│ └────────────────────────┬─────────────────────────┘ │
│ │ │
│ ▼ (dbt dimension & facts) │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Gold Layer: fct_forecast_accuracy & dim_cities │ │
│ └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
▲
│ (Automated Runs & CI/CD)
┌───────────────────────────┴────────────────────────────┐
│ Orchestration & DevOps │
│ - Prefect Cloud: Scheduled Daily Pipeline Execution │
│ - GitHub Actions: CI (Pytest, dbt test, SQLFluff) │
└────────────────────────────────────────────────────────┘

```
┌────────────────┐
│ Open-Meteo │
│ REST API │
└───────┬────────┘
│ (HTTP GET - Hourly Weather JSON)
▼
┌────────────────────────────────────────────────────────┐
│ Extraction & Ingestion │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Python OOP Extractor (Prefect Task) │ │
│ │ - Retries, Backoff, Schema Validation (Pydantic)│ │
│ └────────────────────────┬─────────────────────────┘ │
└───────────────────────────┼────────────────────────────┘
│
▼ (Raw GCS Upload)
┌────────────────────────────────────────────────────────┐
│ Google Cloud Storage (Data Lake) │
│ gs://weather-lake-raw/year=YYYY/month=MM/day=DD/ │
└───────────────────────────┬────────────────────────────┘
│
▼ (GCS-to-BigQuery Load Task)
┌────────────────────────────────────────────────────────┐
│ Google BigQuery (Lakehouse) │
│ │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Bronze Layer: raw_layer.raw_weather (JSON string)│ │
│ └────────────────────────┬─────────────────────────┘ │
│ │ │
│ ▼ (dbt transformations) │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Silver Layer: stg_actuals & stg_forecasts │ │
│ └────────────────────────┬─────────────────────────┘ │
│ │ │
│ ▼ (dbt dimension & facts) │
│ ┌──────────────────────────────────────────────────┐ │
│ │ Gold Layer: fct_forecast_accuracy & dim_cities │ │
│ └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
▲
│ (Automated Runs & CI/CD)
┌───────────────────────────┴────────────────────────────┐
│ Orchestration & DevOps │
│ - Prefect Cloud: Scheduled Daily Pipeline Execution │
│ - GitHub Actions: CI (Pytest, dbt test, SQLFluff) │
└────────────────────────────────────────────────────────┘
```
