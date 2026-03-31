import pytest
from main import get_weather


def test_get_weather(mocker):
    # Mock requests.get
    mock_get = mocker.patch("main.requests.get")
    
    # Set return values
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temperature": 25, "condition": "Sunny"}
    
    # Call function
    result = get_weather("Dubai")
    
    # Assertions
    assert result == {"temperature": 25, "condition": "Sunny"}
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")


def test_get_weather_error(mocker):
    # Mock requests.get to return error status
    mock_get = mocker.patch("main.requests.get")
    mock_get.return_value.status_code = 404
    
    # Verify it raises ValueError
    with pytest.raises(ValueError) as excinfo:
        get_weather("UnknownCity")
    
    assert str(excinfo.value) == "Could not fetch weather data"
