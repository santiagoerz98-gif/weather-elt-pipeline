Here is a technical API documentation draft for the **Open-Meteo Integration** in your Data Engineering project:

---

### **Open-Meteo API Specification**

#### **1. Endpoint**

* **Base URL:** `[https://api.open-meteo.com/v1/forecast](https://api.open-meteo.com/v1/forecast)`
* **Protocol:** HTTPS GET

#### **2. Authentication Requirements**

* **None (Free Tier):** Does not require an API key or token authentication for standard usage.

#### **3. Required Parameters**

* **`latitude`** *(float)*: Latitude of the target location (e.g., `40.4168` for Madrid).
* **`longitude`** *(float)*: Longitude of the target location (e.g., `-3.7038` for Madrid).
* **`hourly`** *(string, comma-separated)*: List of hourly weather metrics to retrieve.

#### **4. Available Weather Variables (MVP Scope)**

* **`temperature_2m`**: Air temperature at 2 meters above ground (°C).
* **`relative_humidity_2m`**: Relative humidity at 2 meters above ground (%).
* **`precipitation`**: Total precipitation (rain, showers, snow) accumulated over the hour (mm).
* **`surface_pressure`**: Atmospheric air pressure at surface level (hPa).
* **`wind_speed_10m`**: Wind speed at 10 meters above ground (km/h).
* **`weather_code`**: Weather condition category based on WMO (World Meteorological Organization) codes.
* **`apparent_temperature`**: "Feels like" temperature (°C).
* **`is_day`**: Day/Night indicator (`1` for day, `0` for night).

#### **5. Date Parameters**

* **`past_days`** *(integer, range 0–92)*: Number of past days of actual observed measurements to include (e.g., `past_days=1` retrieves the previous 24 hours of historical actuals).
* **`forecast_days`** *(integer, range 0–16)*: Number of future days of predicted weather to include (e.g., `forecast_days=0` excludes future predictions; `forecast_days=1` retrieves tomorrow's forecast).

#### **6. Timezone Behavior**

* **`timezone`** *(string)*: Parameter forced to `UTC` (e.g., `timezone=UTC`) to ensure uniform timestamp normalization across all city locations prior to loading into BigQuery.

#### **7. Response Structure**

The API returns a JSON payload containing location metadata, unit descriptors, and aligned array time-series:

```json
{
  "latitude": 40.4168,
  "longitude": -3.7038,
  "generationtime_ms": 0.142,
  "utc_offset_seconds": 0,
  "timezone": "UTC",
  "timezone_abbreviation": "UTC",
  "elevation": 667.0,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "relative_humidity_2m": "%",
    "precipitation": "mm",
    "surface_pressure": "hPa",
    "wind_speed_10m": "km/h",
    "weather_code": "wmo code",
    "apparent_temperature": "°C",
    "is_day": ""
  },
  "hourly": {
    "time": ["2026-08-24T00:00", "2026-08-24T01:00"],
    "temperature_2m": [21.5, 20.8],
    "relative_humidity_2m": [58, 62],
    "precipitation": [0.0, 0.0],
    "surface_pressure": [945.2, 945.0],
    "wind_speed_10m": [12.4, 11.1],
    "weather_code": [0, 0],
    "apparent_temperature": [21.0, 20.3],
    "is_day": [0, 0]
  }
}

```

#### **8. Error Responses**

The API uses standard HTTP status codes along with a JSON error body:

* **HTTP 400 Bad Request:** Returned when coordinates or variable names are invalid/malformed.
```json
{
  "error": true,
  "reason": "Parameter 'hourly' contains invalid variable name."
}

```


* **HTTP 429 Too Many Requests:** Returned when call frequency thresholds are exceeded.
* **HTTP 500 Internal Server Error:** Open-Meteo infrastructure errors.

#### **9. Rate Limits / Usage Restrictions**

* **Non-Commercial Limit:** Up to **10,000 daily API calls** allowed without cost.
* **Concurrency:** Maximum **5,000 requests per hour** and **less than 600 requests per minute**.
* **Impact on Pipeline:** With 4 cities executed daily via Prefect (1–2 API calls per city), overall consumption remains far below 0.1% of the daily allowance.
