import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import API_BASE_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__) 
# The logger is configured to log messages for this module.
# It allows to track the flow of execution and capture any errors or important events that occur during the execution of the code.


class WeatherAPIClient:
    """
    A client for interacting with the Open-Meteo weather API.
    This class handles the construction of API requests, sending them, and processing the responses.
    """

    def __init__(self):
        """
        Initializes the WeatherAPIClient with a session that has retry logic.
        """
        self.base_url = API_BASE_URL
        # The base URL for the Open-Meteo API is set from the configuration settings.
        # It allows for easy updates to the API endpoint without changing the code.

        self.session = requests.Session()
        # The session object is used to persist certain parameters across requests, such as headers and cookies.
        # Without a session, each request would be independent, and we would lose the benefits of connection pooling and retry logic.

        retries = Retry(
            total=5, 
            # The total number of retry attempts for failed requests. 
            # Means that if a request fails, it will be retried up to 5 times before giving up.
            
            backoff_factor=1.0,
            # The backoff factor controls the delay between retry attempts.
            # For example, with a backoff factor of 1.0, the delay will be 1 second after the first failure, 2 seconds after the second failure, 4 seconds after the third failure, and so on.
            # This helps to avoid overwhelming the server with rapid repeated requests and allows time for transient issues to resolve.
            # Transient means temporary issues that may resolve themselves, such as network congestion or server overload.
     
            status_forcelist=[429, 500, 502, 503, 504],
            # The list of HTTP status codes that should trigger a retry.
            # 429: Too Many Requests - indicates that the client has sent too many requests in a given amount of time.
            # 500: Internal Server Error - indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
            # 502: Bad Gateway - indicates that the server received an invalid response from an inbound server.
            # 503: Service Unavailable - indicates that the server is currently unable to handle the request due to temporary overloading or maintenance.
            # 504: Gateway Timeout - indicates that the server did not receive a timely response from an upstream server.
        )
        # Configures the retry logic for the session.

        self.adapter = HTTPAdapter(
            max_retries=retries, 
            # Configures the adapter to retry failed requests up to 5 times with exponential backoff for specific HTTP status codes. 
            # This helps to handle transient errors and improve the reliability of API requests.
            pool_connections=10, 
            # Configures the maximum number of connections to keep in the connection pool. 
            # This helps to reuse connections for multiple requests, improving performance.
            pool_maxsize=10, 
            # Configures the maximum number of connections to keep in the connection pool.
            # For example, if you have a high volume of requests, increasing this value can help to avoid connection errors.
            pool_block=True
            # Configures the adapter to block when the connection pool is exhausted, instead of raising an exception.
            # This is useful in scenarios where you want to wait for a connection to become available rather than failing immediately.
        )

        self.session.mount('https://', self.adapter)
        # Mounts the adapter to handle both HTTP and HTTPS requests, ensuring that the retry logic is applied to all requests made through the session.
        # This is important because the Open-Meteo API uses HTTPS, and we want to ensure that our retry logic is applied to all requests, regardless of the protocol used.

        self.session.mount('http://', self.adapter)

    def get_weather_data(
            self, 
            params:dict | None = None
        )-> dict:
        """
        Sends a GET request to the base URL with optional query parameters.

        Args:
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            dict: The JSON response from the API if the request is successful.

        Raises:
            requests.exceptions.RequestException: If there is an issue with the request.
        """
        url = self.base_url
        # Constructs the full URL for the API request using the base URL.
        # The base URL is defined in the configuration settings and points to the Open-Meteo API endpoint for weather forecasts.

        try:
            logger.info(f"Sending GET request to {url} with params: {params}")
            # Logs an informational message indicating that a GET request is being sent to the specified URL with the provided query parameters.
            # This can be seen in the logs and helps to track the flow of execution and debug issues if they arise.

            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            # Sends a GET request to the constructed URL with optional query parameters and a timeout of 10 seconds.
            # The timeout ensures that the request does not hang indefinitely if the server does not respond.

            response.raise_for_status()
            # Raises an HTTPError if the response status code indicates an error (4xx or 5xx).
            # This allows to handle errors gracefully and log them for debugging purposes.
            # If the response is successful (status code 200), the code will continue to the next step. Else, it will raise an exception that can be caught and handled appropriately.

            try:
                return response.json()
                # Returns the JSON content of the response if the request is successful.
            except ValueError as e:
                logger.exception(f"Failed to parse JSON response from {url} with params: {params}. Exception: {e}")
                # Logs an error message if the response content is not valid JSON.
                # Indicates that the server returned a response that could not be parsed as JSON, which may be due to an unexpected response format or an error on the server side.
                raise ValueError(
                    f"Failed to parse JSON response from {url} with params: {params}. Exception: {e}"
                ) from e

        except requests.exceptions.Timeout as e:
            logger.exception(f"Request to {url} with params: {params} timed out. Exception: {e}")
            # Logs an error message if the request times out.
            # This is important for debugging and monitoring purposes, as it indicates that the server did not respond within the specified timeout period.
            # Reason for timeout could be network issues, server overload, or a slow response from the API.
            raise requests.exceptions.Timeout(
                f"Request to {url} with params: {params} timed out. Exception: {e}"
            ) from e
        
        except requests.exceptions.HTTPError as e:
            logger.exception(f"HTTP error occurred while making GET request to {url} with params: {params}. Exception: {e}")
            # Logs an error message if the response status code indicates an HTTP error (4xx or 5xx).
            # Indicates that the server returned an error response, which could be due to various reasons such as invalid parameters, authentication issues, or server-side problems.
            raise requests.exceptions.HTTPError(
                f"HTTP error occurred while making GET request to {url} with params: {params}. Exception: {e}"
            ) from e

        except requests.exceptions.RequestException as e:
            logger.exception(f"Error occurred while making GET request to {url} with params: {params}. Exception: {e}")
            # Logs an error message if there is an issue with the request, such as a connection error or timeout.
            # This is a catch-all for any other exceptions that may occur during the request process, allowing to handle unexpected issues gracefully.
            raise requests.exceptions.RequestException(
                f"An error occurred while making GET request to {url} with params: {params}. Exception: {e}"
            ) from e

    def get_historical_weather(
            self, 
            latitude: float, 
            longitude: float,
            weather_params: dict, 
            timezone: str | None = "UTC",
            past_days: int | None = 1
        ) -> dict:
        """
        Fetches historical weather data for the specified latitude and longitude. 

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            weather_params (dict): A dictionary of weather parameters to request from the API.
            timezone (str, optional): The timezone for the API response. Defaults to "UTC".
            past_days (int, optional): The number of past days to request weather data for. Defaults to 1.

        Returns:
            dict: A dictionary containing the historical weather data.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(weather_params),
            "timezone": timezone,
            "past_days": past_days,
            "forecast_days": 0,  # No forecast days requested for historical data
        }

        return self.get_weather_data(params=params)

    def get_forecast_weather(
            self, 
            latitude: float, 
            longitude: float,
            weather_params: dict, 
            timezone: str | None = "UTC",
            forecast_days: int | None = 7
        ) -> dict:
        """
        Fetches forecast weather data for the specified latitude and longitude. 

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            weather_params (dict): A dictionary of weather parameters to request from the API.
            timezone (str, optional): The timezone for the API response. Defaults to "UTC".
            forecast_days (int, optional): The number of forecast days to request weather data for. Defaults to 7. Maximum allowed is 16 days as per the API documentation.

        Returns:
            dict: A dictionary containing the forecast weather data.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(weather_params),
            "timezone": timezone,
            "forecast_days": forecast_days,
            "past_days": 0,  # No past days requested for forecast data
        }

        return self.get_weather_data(params=params)