from poll_weather import get_weather_data

data = get_weather_data()

from pprint import pprint
from datetime import datetime

count = 0

for forecast in data['hourly']:
    # pprint(forecast['dt'])
    hour = datetime.fromtimestamp(forecast['dt'])
    pprint(hour)
    print(forecast['temp'])
    count += 1
    if count == 24:
        break



