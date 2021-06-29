from src.main import Weather


def test_will_it_rain(mocker):
    mocker.patch('Weather._get_city_woeid', return_value=666)
    city = 'london'
    weather = Weather(city)
    assert weather._get_city_woeid() == 666
    # assert weather.will_it_rain() is True
