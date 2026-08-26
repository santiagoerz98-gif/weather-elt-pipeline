from pydantic import BaseModel, model_validator, ValidationError
from typing import Optional

# Define the Pydantic model for the hourly weather data
# The HourlyWeather model represents the structure of the hourly weather data returned by the API. Each attribute corresponds to a specific weather parameter, and the types are defined to ensure that the data is validated correctly.
# This model will be used to validate the response data from the weather API, ensuring that all expected keys are present and that the data types are correct. 
# If any required keys are missing or if the data types do not match, a ValidationError will be raised, indicating that the response data is not in the expected format.
class HourlyWeather(BaseModel):
    time: list[str]
    temperature_2m: list[Optional[float]]
    relative_humidity_2m: list[Optional[float]]
    precipitation: list[Optional[float]]
    surface_pressure: list[Optional[float]]
    wind_speed_10m: list[Optional[float]]
    apparent_temperature: list[Optional[float]]
    is_day: list[Optional[int]]
    weather_code: list[Optional[int]]

    # The validate_series_length method is a custom validator that checks if all the lists in the HourlyWeather model have the same length as the 'time' list. 
    # This ensures that each weather parameter has a corresponding value for each time point. 
    # If any of the lists have a different length, a ValidationError is raised, indicating that the data is inconsistent.
    @model_validator(mode="after")
    def validate_series_length(self):
        expected_length = len(self.time)
        for field_name, field_value in self.__dict__.items():   
            if field_name != "time" and len(field_value) != expected_length:
                raise ValidationError(f"Length of '{field_name}' does not match length of 'time'. Expected {expected_length}, got {len(field_value)}.")
            
        # Return the instance of the model after validation. This allows for method chaining and ensures that the validated data can be used immediately after validation.   
        return self 
        

# The WeatherResponse model represents the overall structure of the weather data response from the API. It includes metadata about the response, such as latitude, longitude, timezone, and elevation, as well as the hourly weather data encapsulated in the HourlyWeather model.
# This model will be used to validate the entire response from the weather API, ensuring that all expected keys are present and that the data types are correct.
# If any required keys are missing or if the data types do not match, a ValidationError will be raised, indicating that the response data is not in the expected format.
class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    hourly_units: dict[str, str]
    hourly: HourlyWeather
