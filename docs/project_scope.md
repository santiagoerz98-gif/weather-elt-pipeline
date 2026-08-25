Here is the defined scope for your Minimum Viable Product (MVP):

**1. Target Locations (4 Cities)**

- **Madrid, Spain** (Latitude: 40.4168, Longitude: -3.7038)
- **New York, USA** (Latitude: 40.7128, Longitude: -74.0060)
- **Tokyo, Japan** (Latitude: 35.6762, Longitude: 139.6503)
- **London, UK** (Latitude: 51.5074, Longitude: -0.1278)

_Selection Rationale:_ Provides a diverse mix of geographic zones, climate patterns, and time zones to test API extraction and temporal transformations in dbt.

---

**2. Weather Variables**
To keep the initial schema lean yet rich enough for dimensional modeling, collect the following core metrics:

- **Primary Metrics:**
- `temperature_2m` (°C)
- `relative_humidity_2m` (%)
- `precipitation` (mm)
- `surface_pressure` (hPa)
- `wind_speed_10m` (km/h)
- `apparent_temperature` (°C)
- `is_day` (0 or 1)

- **Metadata / Categorical:**
- `weather_code` (WMO code representing weather condition: clear, rain, snow, etc.)

---

**3. Data Granularity**

- **Time Interval:** **Hourly** (`hourly` parameter in Open-Meteo API).
- **Execution Frequency:** Daily batch run via Prefect, fetching the previous 24 hours of data.
- **Record Structure:** Each row in the raw/staging layer represents **1 City + 1 Hour timestamp**.
