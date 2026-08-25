
# This file contains configuration settings for the application.
# Separates configuration from code for easier management and maintenance.

API_BASE_URL = "https://api.open-meteo.com/v1/forecast" # The base URL for the Open-Meteo API, which provides weather forecast data.

REQUEST_TIMEOUT = 10  # The maximum time (in seconds) to wait for a response from the API before timing out.

LOCATIONS = {
    "Madrid": {"latitude": 40.4168, "longitude": -3.7038},  # Coordinates for Madrid, Spain.
    "New York": {"latitude": 40.7128, "longitude": -74.0060},  # Coordinates for New York City, USA.
    "Tokyo": {"latitude": 35.6895, "longitude": 139.6917},  # Coordinates for Tokyo, Japan.
    "London": {"latitude": 51.5074, "longitude": -0.1278},  # Coordinates for London, UK.
}

# Weather codes mapping to their corresponding descriptions. These codes are used in the API response to indicate specific weather conditions. 
# It will ease the gold layer interpretation of the weather data by providing human-readable descriptions.
WEATHER_CODES = {
    0: "Clear sky",  # Weather code 0 corresponds to clear sky conditions
    1: "Mainly clear",  # Weather code 1 corresponds to mainly clear conditions
    2: "Partly cloudy",  # Weather code 2 corresponds to partly cloudy conditions
    3: "Overcast",  # Weather code 3 corresponds to overcast conditions
    45: "Fog",  # Weather code 45 corresponds to fog
    48: "Depositing rime fog",  # Weather code 48 corresponds to depositing rime fog
    51: "Drizzle: Light",  # Weather code 51 corresponds to light drizzle
    53: "Drizzle: Moderate",  # Weather code 53 corresponds to moderate drizzle
    55: "Drizzle: Dense",  # Weather code 55 corresponds to dense drizzle
    56: "Freezing Drizzle: Light",  # Weather code 56 corresponds to light freezing drizzle
    57: "Freezing Drizzle: Dense",  # Weather code 57 corresponds to dense freezing drizzle
    61: "Rain: Slight",  # Weather code 61 corresponds to slight rain
    63: "Rain: Moderate",  # Weather code 63 corresponds to moderate rain
    65: "Rain: Heavy",  # Weather code 65 corresponds to heavy rain
    66: "Freezing Rain: Light",  # Weather code 66 corresponds to light freezing rain
    67: "Freezing Rain: Heavy",  # Weather code 67 corresponds to heavy freezing rain
    71: "Snow fall: Slight",  # Weather code 71 corresponds to slight snowfall
    73: "Snow fall: Moderate",  # Weather code 73 corresponds to moderate snowfall
    75: "Snow fall: Heavy",  # Weather code 75 corresponds to heavy snowfall
    77: "Snow grains",  # Weather code 77 corresponds to snow grains
    80: "Rain showers: Slight",  # Weather code 80 corresponds to slight rain showers
    81: "Rain showers: Moderate",  # Weather code 81 corresponds to moderate rain showers
    82: "Rain showers: Violent",  # Weather code 82 corresponds to violent rain showers
    85: "Snow showers: Slight",  # Weather code 85 corresponds to slight snow showers
    86: "Snow showers: Heavy",  # Weather code 86 corresponds to heavy snow showers
    95: "Thunderstorm: Slight or moderate",  # Weather code 95 corresponds to slight or moderate thunderstorms
    96: "Thunderstorm with slight hail",  # Weather code 96 corresponds to thunderstorms with slight hail
    99: "Thunderstorm with heavy hail",  # Weather code 99 corresponds to thunderstorms with heavy hail
}

# List of hourly weather parameters to request from the API. These parameters provide detailed weather information for each hour of the forecast.
# It will be used to construct the query parameters for the API request.
WEATHER_PARAMETERS = [
    "temperature_2m",  # Temperature at 2 meters above ground level
    "relative_humidity_2m",  # Relative humidity at 2 meters above ground level
    "precipitation",  # Precipitation amount
    "surface_pressure",  # Surface pressure
    "wind_speed_10m",  # Wind speed at 10 meters above ground level
    "apparent_temperature",  # Apparent temperature
    "is_day",  # Day indicator (0 for night, 1 for day)
]

HISTORICAL_QUERY_PARAMS = {
    "hourly": ",".join(WEATHER_PARAMETERS),  # Join the list of weather parameters into a comma-separated string for the API request.
    "timezone": "UTC",  # Set the timezone for the API response to Coordinated Universal Time (UTC). This ensures that the weather data is returned in a consistent time format regardless of the location.
    "past_days": 1,  # Request weather data for the past 1 day. This allows for historical weather analysis.
    "forecast_days": 0,  # Request no forecast days. This is set to 0 because we are only interested in historical data for this query.
}

FORECAST_QUERY_PARAMS = {
    "hourly": ",".join(WEATHER_PARAMETERS),  # Join the list of weather parameters into a comma-separated string for the API request.
    "timezone": "UTC",  # Set the timezone for the API response to Coordinated Universal Time (UTC). This ensures that the weather data is returned in a consistent time format regardless of the location.
    "forecast_days": 7,  # Request weather forecast data for the next 7 days. This allows for short-term weather predictions.
    "past_days": 0,  # Request no past days. This is set to 0 because we are only interested in forecast data for this query.
}

