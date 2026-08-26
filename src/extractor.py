from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime, timezone
from src.weather_schema import WeatherResponse, ValidationError

@dataclass
class ExtractionResult:
    """
    A dataclass to hold the result of the extraction process.
    
    Attributes:
        city (str): The name of the city for which the data was extracted.
        latitude (float): The latitude of the city.
        longitude (float): The longitude of the city.
        data_type (str): The type of data extracted (e.g., "historical", "forecast").
        extracted_at (datetime): The timestamp when the extraction was performed.
        payload (Dict[str, Any]): The extracted weather data.
    """
    city: str
    latitude: float
    longitude: float
    data_type: str
    extracted_at: datetime
    payload: Dict[str, Any]

class WeatherExtractor:
    """
    A class responsible for extracting weather data.

    Methods:
        extract(city: str, latitude: float, longitude: float, data_type: str) -> ExtractionResult:
            Extracts weather data for the specified city and returns an ExtractionResult.
    """
    def __init__(self, client):
        self.client = client

    def extract_historical(
            self, 
            city: str, 
            latitude: float, 
            longitude: float, 
            weather_params: dict,
            timezone: str | None = "UTC",
            past_days: int | None = 1
        ) -> ExtractionResult:
        """
        Extracts weather data for the specified city and returns an ExtractionResult.

        Args:
            city (str): The name of the city for which to extract weather data.
            latitude (float): The latitude of the city.
            longitude (float): The longitude of the city.
            weather_params (dict): The weather parameters to extract.
            timezone (str | None): The timezone for the extraction. Defaults to "UTC".
            past_days (int | None): The number of past days to extract. Defaults to 1.

        Returns:
            ExtractionResult: The result of the extraction process.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(weather_params),
            "timezone": timezone,
            "past_days": past_days,
            "forecast_days": 0  # For historical extraction, we do not need forecast days, so we set it to 0.
        }

        payload = self.client.get_weather_data(params)

        # pydantic validation
        try:
            validated_payload = WeatherResponse(**payload) # **payload unpacks the dictionary into keyword arguments for the WeatherResponse model, allowing for validation of the payload structure and data types.
        except ValidationError as e:
            raise ValueError(f"Payload validation failed: {e}") from e

        return ExtractionResult(
            city=city,
            latitude=latitude,
            longitude=longitude,
            data_type="historical",
            extracted_at=datetime.now().isoformat(),
            payload=validated_payload.model_dump()
        )

    def extract_forecast(
            self, 
            city: str, 
            latitude: float, 
            longitude: float, 
            weather_params: dict,
            timezone: str | None = "UTC",
            forecast_days: int | None = 7
        ) -> ExtractionResult:
        """
        Extracts weather forecast data for the specified city and returns an ExtractionResult.

        Args:
            city (str): The name of the city for which to extract weather forecast data.
            latitude (float): The latitude of the city.
            longitude (float): The longitude of the city.
            weather_params (dict): The weather parameters to extract.
            timezone (str | None): The timezone for the extraction. Defaults to "UTC".
            forecast_days (int | None): The number of forecast days to extract. Defaults to 7. Maximum allowed is 16.

        Returns:
            ExtractionResult: The result of the extraction process.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(weather_params),
            "timezone": timezone,
            "past_days": 0,  # For forecast extraction, we do not need past days, so we set it to 0.
            "forecast_days": forecast_days
        }

        payload = self.client.get_weather_data(params)

        # pydantic validation
        try:
            validated_payload = WeatherResponse(**payload) # **payload unpacks the dictionary into keyword arguments for the WeatherResponse model, allowing for validation of the payload structure and data types.
        except ValidationError as e:
            raise ValueError(f"Payload validation failed: {e}") from e

        return ExtractionResult(
            city=city,
            latitude=latitude,
            longitude=longitude,
            data_type="forecast",
            extracted_at=datetime.now().isoformat(),
            payload=validated_payload.model_dump()
        )


