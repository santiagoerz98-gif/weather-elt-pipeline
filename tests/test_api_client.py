from src.api_client import WeatherAPIClient
from config.settings import LOCATIONS, WEATHER_PARAMETERS

client = WeatherAPIClient()

def test_get_weather_data():
    # Test fetching weather data for Madrid
    location = "Madrid"
    data = client.get_historical_weather(
        latitude=LOCATIONS[location]["latitude"],
        longitude=LOCATIONS[location]["longitude"],
        weather_params=WEATHER_PARAMETERS
    )

    # Validate the response data. 
    # 'assert' statements are used to ensure that the expected keys are present in the response data. 
    # If any of these assertions fail, it indicates that the API response is missing expected weather parameters, which could be due to an issue with the API or the request. 
    assert data is not None, "Weather data should not be None"
    assert "temperature_2m" in data['hourly'], "Temperature data should be present in the response" 
    assert "relative_humidity_2m" in data['hourly'], "Relative humidity data should be present in the response"
    assert "precipitation" in data['hourly'], "Precipitation data should be present in the response"
    assert "surface_pressure" in data['hourly'], "Surface pressure data should be present in the response"
    assert "wind_speed_10m" in data['hourly'], "Wind speed data should be present in the response"
    assert "apparent_temperature" in data['hourly'], "Apparent temperature data should be present in the response"
    assert "is_day" in data['hourly'], "Day indicator should be present in the response"

    return data  # Return the data for further inspection if needed

if __name__ == "__main__":
    # Run the test function and print the results for manual inspection
    weather_data = test_get_weather_data()
    print("Weather data fetched successfully:")
    print(weather_data)