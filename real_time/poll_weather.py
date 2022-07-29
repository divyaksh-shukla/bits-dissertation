from logging import log
import logging
import os
import requests
import json
import csv
from pprint import pprint
from kafka import KafkaProducer, TopicPartition
from time import sleep
from datetime import datetime, timedelta

API_KEY = "34120c061da5c3d6ed3be40169616d5f"
MODE='json'
COUNT='48'

# Houston airport coordinates
LAT = 29.9902
LON = -95.3368

API_URL = 'https://pro.openweathermap.org/data/2.5/forecast/hourly'

DELAY_TIME = 3600

KAFKA_BOOTSTRAP_SERVER = 'localhost:9092'

PROJECT_DIR = '/home/divyaksh/Documents/Coding/python/forecasting'
count = 0
LOG_FILENAME = os.path.join(PROJECT_DIR, 'real_time', 'poll_weather.log')
DATA_FILENAME = os.path.join(PROJECT_DIR, 'real_time','weather_data.json')
CSV_FILENAME = os.path.join(PROJECT_DIR, 'real_time','real_time_weather.csv')

HEADERS = ['dt_iso','city_name','lat','lon','temp','visibility','dew_point','feels_like','temp_min','temp_max','pressure','sea_level','grnd_level','humidity','wind_speed','wind_deg','wind_gust','rain_1h','rain_3h','snow_1h','snow_3h','clouds_all','weather_id','weather_main','weather_description','weather_icon']

def get_weather_data():
    global result
    retry_count = 3
    while (retry_count !=0):
        try:
            result = requests.get(API_URL, {'lat': LAT, 'lon': LON, 'appid': API_KEY, 'mode': MODE, 'cnt': COUNT})
            retry_count -= 1
            break
        except:
            continue
    data = json.loads(result.text)
    return data

def configure_kafka_producer():
    global producer
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER, value_serializer=lambda x: json.dumps(x).encode('utf-8'), connections_max_idle_ms=10**9)
    except:
        logger.exception("Error in creating kafka producer")

def put_into_kafka(data, topic='input-houston-weather'):
    global producer
    if (not(producer.bootstrap_connected())):
        producer.close()
        producer.__del__()
        configure_kafka_producer()
    if (producer.bootstrap_connected()):
        producer.send(topic=topic, value=data)
        producer.flush()

def put_data_into_file(data, filename):
    _file = open(filename, 'r')
    # pprint(data)
    output = []
    output.append(HEADERS)
    
    csv_reader = csv.reader(_file)
    logger.debug('Established csv reader')
    
    current_data = parse_data_to_array(data['list'][0])

    logger.debug(f'reading from {_file.name} using csv_reader')
    for i, row in enumerate(csv_reader):
        if (i == 0):
            continue
        row_time = datetime.fromisoformat(row[0])
        current_time = datetime.fromisoformat(current_data[0])

        if (current_time == row_time):
            logger.debug(f'Current time = {current_time}, row time = {row_time}')
            break
        else:
            output.append(row)
    
    for hd in data['list']:
        output.append(parse_data_to_array(hd))
    
    _file.close()
    _file = open(filename, 'w')
    csv_writer = csv.writer(_file)
    csv_writer.writerows(output)
    
    _file.close()

def parse_data_to_array(data):
    date_obj = datetime.fromtimestamp(data['dt'])
    weather = data['weather'][0]
    timediff = -21600
    local_time = date_obj + timedelta(seconds=timediff)
    return [
        local_time.isoformat(),
        'Houston airport',
        LAT, LON,
        data['main']['temp'],
        data['visibility'],
        '',
        data['main']['feels_like'],
        data['main']['temp_min'],
        data['main']['temp_max'],
        data['main']['pressure'],
        data['main']['sea_level'],
        data['main']['grnd_level'],
        data['main']['humidity'],
        data['wind']['speed'],
        data['wind']['deg'],
        data['wind']['gust'],
        '','','','',
        data['clouds']['all'],
        weather['main'],
        weather['description'],
        weather['icon'],
    ]

def scheduled_loop():
    global count
    #Loop
    data = get_weather_data()
    # put_into_kafka(data)
    put_data_into_file(data, CSV_FILENAME)
    count += 1
    logger.info(f'Data count :{count}')

if __name__ == '__main__':
    #Setup
    logging.basicConfig(filename=LOG_FILENAME, filemode='a', level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    logger = logging.getLogger(name="poll_weather")
    # configure_kafka_producer()

    scheduled_loop()
    
    

