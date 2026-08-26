from config.settings import WEATHER_PARAMETERS, LOCATIONS
from src.extractor import WeatherExtractor
from datetime import datetime
from src.api_client import WeatherAPIClient

client = WeatherAPIClient()

extractor = WeatherExtractor(client)

def test_extract_weather_data():
    # Test extracting weather data for Madrid
    location = "Madrid"
    latitude = LOCATIONS[location]["latitude"]
    longitude = LOCATIONS[location]["longitude"]

    return extractor.extract_historical(
        past_days=1,
        city=location,
        latitude=latitude,
        longitude=longitude,
        weather_params=WEATHER_PARAMETERS
    )

if __name__ == "__main__":
    # Run the test function and print the results for manual inspection
    extraction_result = test_extract_weather_data()
    print("Weather data extracted successfully:")
    print(extraction_result)