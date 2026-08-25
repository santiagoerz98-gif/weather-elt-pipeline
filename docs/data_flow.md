```
[Open-Meteo REST API]
       │
       │ (1) Extraction (Python OOP script in Prefect Task)
       ▼
[Google Cloud Storage (GCS)] ──► Raw JSON Payloads (`gs://bucket/raw/YYYY/MM/DD/`)
       │
       │ (2) Ingestion / Landing
       ▼
[BigQuery - Landing / Bronze] ──► `raw_weather_json` (Unparsed JSON table)
       │
       │ (3) Transformation (dbt Models)
       ├──► Staging (Silver): `stg_actual_weather` & `stg_forecast_weather` (Parsed, Cleaned & Cast)
       └──► Marts (Gold):   `fct_weather_hourly`, `fct_forecast_accuracy` & `dim_cities`

```

---

### Phase-by-Phase Breakdown

#### 1. Source System (API)

- **Source:** Open-Meteo Weather Forecast API.
- **Format:** Nested JSON HTTP responses (hourly array vectors).
- **Extraction Strategy:** Python `@task` in Prefect issuing GET requests with explicit location parameters (`latitude`, `longitude`, `hourly` variables, `timezone=UTC`).

#### 2. Data Lake Layer (Raw Storage / GCS)

- **Target Container:** Google Cloud Storage bucket.
- **Storage Path:** `gs://<your-bucket-name>/raw_weather/<data_type>/year=YYYY/month=MM/day=DD/<city>_<timestamp>.json`
- **Format:** Unaltered, compressed raw JSON files (preserves complete lineage for auditability and replayability).

#### 3. Data Warehouse Layer (BigQuery - Bronze / Landing)

- **Target Table:** `raw_layer.raw_weather`
- **Transformation:** External or native loading into BigQuery.
- **Schema:**
- `ingestion_timestamp` (TIMESTAMP)
- `source_city` (STRING)
- `data_type` (STRING: `ACTUAL` or `FORECAST`)
- `raw_payload` (JSON / STRING)

#### 4. Transformation Layer (dbt - Silver / Staging)

- **dbt Staging Models:** `stg_actual_weather.sql`, `stg_forecast_weather.sql`
- **Operations:**
- Unnesting JSON array objects into tabular rows (1 row = 1 City + 1 Target Hour).
- Datatype casting (ISO strings to `TIMESTAMP`, numbers to `FLOAT64` / `INT64`).
- Renaming fields to standard domain conventions (e.g., `temperature_2m` to `temperature_celsius`).
- Deduplication via window functions (`QUALIFY ROW_NUMBER() OVER (...)`).

#### 5. Analytics Marts Layer (dbt - Gold / Marts)

- **Target Tables:**
- **`dim_cities` (Dimension Table):** Master metadata for target coordinates (Madrid, New York, Tokyo, London).
- **`fct_weather_hourly` (Fact Table):** Partitioned historical facts for actual readings, aggregated daily/monthly.
- **`fct_forecast_accuracy` (Fact Table):** Joined facts comparing predicted vs. actual metrics on `(city, target_timestamp)`, computing error metrics (MAE, absolute variance, accuracy boolean flags).

---

### Target Field Mapping Matrix

| Source API Field       | Raw Layer (BigQuery) | Staging Field (Silver) | Mart Field (Gold)     | Target Datatype |
| ---------------------- | -------------------- | ---------------------- | --------------------- | --------------- |
| N/A (Metadata)         | `source_city`        | `city_name`            | `city_name`           | `STRING`        |
| `latitude`             | JSON key             | `latitude`             | `latitude`            | `FLOAT64`       |
| `longitude`            | JSON key             | `longitude`            | `longitude`           | `FLOAT64`       |
| `time`                 | Array Element        | `target_timestamp`     | `valid_timestamp_utc` | `TIMESTAMP`     |
| `temperature_2m`       | Array Element        | `temperature_2m`       | `temperature_celsius` | `FLOAT64`       |
| `relative_humidity_2m` | Array Element        | `relative_humidity_2m` | `humidity_pct`        | `INT64`         |
| `precipitation`        | Array Element        | `precipitation`        | `precipitation_mm`    | `FLOAT64`       |
| `surface_pressure`     | Array Element        | `surface_pressure`     | `pressure_hpa`        | `FLOAT64`       |
| `wind_speed_10m`       | Array Element        | `wind_speed_10m`       | `wind_speed_kmh`      | `FLOAT64`       |
| `weather_code`         | Array Element        | `weather_code`         | `wmo_code`            | `INT64`         |
| `apparent_temperature` | Array Element        | `apparent_temperature` | `feels_like_celsius`  | `FLOAT64`       |
| `is_day`               | Array Element        | `is_day`               | `is_daytime`          | `BOOLEAN`       |
