# Getting historical data
import json
import requests
from datetime import datetime, timedelta

# Houston airport coordinates
LAT = 29.9902
LON = 95.3368

TYPE = "hour"
START_TIME = datetime.now() - timedelta(days = 365)
END_TIME = datetime.now()

API_KEY = "0551bf040e9ad5db17aaddf95eb1b146"

API_URL = 'http://history.openweathermap.org/data/2.5/history/city'

if __name__ == '__main__':
    start_epoch = int(START_TIME.timestamp())
    end_epoch = int(END_TIME.timestamp())
    print(start_epoch, end_epoch)
    result = requests.get(API_URL, {'lat': LAT, 'lon': LON, 'appid': API_KEY, 'type': 'hour', 'start': start_epoch, 'end': end_epoch})
    
    if (result.status_code == 200):
        data = result.json()
        json.dump(data, open('data.json', 'w'))
        print('success')
