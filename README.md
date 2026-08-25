This project is an end-to-end, modern Data Engineering pipeline designed to ingest, store, transform, and orchestrate weather data using an automated, cloud-native architecture. Its core purpose is to demonstrate a production-ready ELT (Extract, Load, Transform) workflow that turns raw API responses into structured, analytics-ready dimensional models for business intelligence and data science.

* **Data Source (Open-Meteo):** Serves as the primary source for real-time and historical weather API data.
* **Extraction (Python):** Utilizes object-oriented Python scripts to reliably extract JSON payloads with built-in error handling and retries.
* **Raw Storage (Google Cloud Storage):** Functions as the Data Lake layer, securely storing untransformed, raw data payloads.
* **Lakehouse (BigQuery):** Acts as the centralized Data Warehouse/Lakehouse for scalable querying and storage.
* **Transformation (dbt):** Executes SQL-based data transformations directly inside BigQuery, implementing data modeling (Staging to Marts) and quality testing.
* **Orchestration (Prefect):** Manages, schedules, and monitors the end-to-end flow execution and dependencies using Python-native `@flow` and `@task` decorators.
* **CI (GitHub Actions):** Automates code linting, unit testing (`pytest`), and dbt test validations upon code pushes to maintain deployment reliability.