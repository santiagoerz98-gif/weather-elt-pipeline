The initial architecture follows an automated, cloud-native **ELT (Extract, Load, Transform)** pattern. It decouples raw data ingestion from analytical transformations, ensuring high scalability, data lineage tracking, and zero operational infrastructure cost.

---

### **Architectural Diagram**

```
 ┌────────────────┐
 │   Open-Meteo   │
 │   REST API     │
 └───────┬────────┘
         │ (HTTP GET - Hourly Weather JSON)
         ▼
 ┌────────────────────────────────────────────────────────┐
 │               Extraction & Ingestion                   │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │      Python OOP Extractor (Prefect Task)         │  │
 │  │  - Retries, Backoff, Schema Validation (Pydantic)│  │
 │  └────────────────────────┬─────────────────────────┘  │
 └───────────────────────────┼────────────────────────────┘
                             │
                             ▼ (Raw GCS Upload)
 ┌────────────────────────────────────────────────────────┐
 │           Google Cloud Storage (Data Lake)             │
 │  gs://weather-lake-raw/year=YYYY/month=MM/day=DD/      │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼ (GCS-to-BigQuery Load Task)
 ┌────────────────────────────────────────────────────────┐
 │              Google BigQuery (Lakehouse)               │
 │                                                        │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ Bronze Layer: raw_layer.raw_weather (JSON string)│  │
 │  └────────────────────────┬─────────────────────────┘  │
 │                           │                            │
 │                           ▼ (dbt transformations)      │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ Silver Layer: stg_actuals & stg_forecasts        │  │
 │  └────────────────────────┬─────────────────────────┘  │
 │                           │                            │
 │                           ▼ (dbt dimension & facts)    │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ Gold Layer: fct_forecast_accuracy & dim_cities   │  │
 │  └──────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────┘
                             ▲
                             │ (Automated Runs & CI/CD)
 ┌───────────────────────────┴────────────────────────────┐
 │                  Orchestration & DevOps                │
 │  - Prefect Cloud: Scheduled Daily Pipeline Execution   │
 │  - GitHub Actions: CI (Pytest, dbt test, SQLFluff)     │
 └────────────────────────────────────────────────────────┘

```

---

### **Layer-by-Layer Architectural Component Specification**

#### **1. Data Source & Extraction Layer**

- **Component:** Python 3.11+ application structured with Object-Oriented Programming (OOP) design patterns.
- **Responsibility:**
- Issues authenticated/parameterized HTTP requests to the Open-Meteo API for target coordinates (Madrid, NY, Tokyo, London).
- Enforces API robustness via `tenacity` retries and exponential backoff handling for HTTP 429/500 errors.
- Validates structure using `pydantic` models before writing payload buffers.

#### **2. Data Lake Layer (Raw Storage)**

- **Component:** Google Cloud Storage (GCS) Bucket (`Standard` storage class).
- **Partitioning Scheme:** Hive-partitioned directory paths:
  `gs://weather-lakehouse-raw/data_type={actuals|forecast}/year={YYYY}/month={MM}/day={DD}/{city}_{timestamp}.json`
- **Responsibility:** Immutable landing storage. Protects against schema drift and allows pipeline backfills without re-querying the source API.

#### **3. Data Warehouse / Lakehouse Layer**

- **Component:** Google BigQuery.
- **Architecture:** Multi-layered Data Warehouse design:
- **Bronze (Landing):** `raw_layer.raw_weather` table holding ingestion metadata + raw unparsed JSON payloads.
- **Silver (Staging):** `staging_layer.stg_actual_weather` and `stg_forecast_weather`. Tables are **Partitioned by `DATE(target_timestamp)**`and **Clustered by`city\*\*`.
- **Gold (Analytics Marts):** Dimensional models (`fct_weather_hourly`, `fct_forecast_accuracy`, `dim_cities`) optimized for reporting.

#### **4. Transformation Layer**

- **Component:** `dbt-bigquery` (dbt Core).
- **Responsibility:**
- Flattens JSON vectors into relational rows.
- Handles UTC timezone standardization and metric casting.
- Executes data quality tests (`not_null`, `unique`, accepted value ranges for temperatures).
- Computes statistical metrics (Absolute Error, Bias, MAE) for forecast accuracy models.

#### **5. Orchestration Layer**

- **Component:** Prefect 2.x / 3.x (Prefect Cloud orchestration engine).
- **Flow Workflow:**

1. `task_extract_open_meteo()` $\rightarrow$ Ingests API data for all locations.
2. `task_upload_to_gcs()` $\rightarrow$ Persists raw JSON payloads to GCS bucket.
3. `task_load_gcs_to_bigquery()` $\rightarrow$ Loads raw JSON payloads into BigQuery Bronze.
4. `task_trigger_dbt_run()` $\rightarrow$ Invokes `dbt run` & `dbt test` to build Silver/Gold layers.

#### **6. CI/CD & Security Layer**

- **Component:** GitHub Actions & Service Accounts.
- **Responsibility:**
- Triggers automated testing (`pytest` for extractors, `dbt test` for modeling) on every Pull Request.
- Enforces code formatting via `black` and SQL linting via `sqlfluff`.
- Secure authentication via GCP Service Account Keys stored in GitHub Secrets.
