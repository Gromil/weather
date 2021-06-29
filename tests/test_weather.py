from freezegun import freeze_time

from src.main import Weather

london_data = {
    "consolidated_weather": [
        {
            "id": 4883192243814400,
            "weather_state_name": "Light Rain",
            "weather_state_abbr": "lr",
            "created": "2021-06-29T12:32:01.473844Z",
            "applicable_date": "2021-06-29",
        },
        {
            "id": 5713926361710592,
            "weather_state_name": "Showers",
            "weather_state_abbr": "s",
            "created": "2021-06-29T12:32:01.748206Z",
            "applicable_date": "2021-06-30",
        }
    ]
}


@freeze_time("2021-06-29")
def test_will_it_rain(mocker):
    mocker.patch('src.main.Weather._get_city_woeid', return_value=44418)
    mocker.patch(
        'src.main.Weather._get_forecast_data', return_value=london_data
    )

    city = 'london'
    weather = Weather(city)
    assert weather.will_it_rain() is True
