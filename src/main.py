from datetime import datetime, timedelta
from typing import Optional

import click
import requests


class Weather:
    URL = 'https://www.metaweather.com/api/location/'
    RAIN_STATES = ('lr', 'hr', 's')

    def __init__(self, city: str) -> None:
        self.city = city

    def _get_city_woeid(self) -> Optional[int]:
        response = requests.get(
            f'{self.URL}search/', params={'query': self.city}
        )
        response.raise_for_status()
        city_data = response.json()
        return city_data[0]['woeid'] if city_data else None

    def _get_forecast_data(self, woeid: int) -> dict:
        response = requests.get(f'{self.URL}{woeid}/')
        response.raise_for_status()
        return response.json()

    def _get_tomorrows_forecast(self, forecast_data: dict) -> dict:
        tomorrow_date = (
                datetime.today() + timedelta(days=1)
        ).strftime('%Y-%m-%d')
        for daily_forecast in forecast_data['consolidated_weather']:
            if daily_forecast['applicable_date'] == tomorrow_date:
                return daily_forecast

    def will_it_rain(self) -> bool:
        woeid = self._get_city_woeid()
        forecast_data = self._get_forecast_data(woeid)
        data = self._get_tomorrows_forecast(forecast_data)
        if data['weather_state_abbr'] in self.RAIN_STATES:
            return True
        return False


@click.command()
@click.option('--city', help='City to check.')
def main(city):
    weather = Weather(city)
    if weather.will_it_rain() is True:
        print(f'Tomorrow will be rainy day for "{city}"!')
    else:
        print(f'No rain tomorrow for "{city}"!')


if __name__ == '__main__':
    main()
