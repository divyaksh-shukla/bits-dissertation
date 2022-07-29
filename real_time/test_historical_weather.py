from datetime import datetime, timedelta
import csv

FILENAME = 'hoston_historical_weather_6d3043f9e8ce849135c272cf62652f27.csv'
OUTPUT_FILENAME = 'hoston_historical_weather_modified.csv'
FILE = open(FILENAME, 'r')
OUTPUT_FILE = open(OUTPUT_FILENAME, 'w')
lines = FILE.readlines()
data = csv.reader(lines)
csv_writer = csv.writer(OUTPUT_FILE)

HEADERS = ['dt_iso','city_name','lat','lon','temp','visibility','dew_point','feels_like','temp_min','temp_max','pressure','sea_level','grnd_level','humidity','wind_speed','wind_deg','wind_gust','rain_1h','rain_3h','snow_1h','snow_3h','clouds_all','weather_id','weather_main','weather_description','weather_icon']

count = 1
for row in data:
    if (count == 1):
        csv_writer.writerow(HEADERS)
    else:
        utc_date = datetime.fromisoformat(row[1][:19])
        timediff = int(row[2])
        local_time = utc_date + timedelta(seconds=timediff)
        modified_row = [local_time.isoformat()]
        print(local_time)
        modified_row.extend(row[3:])
        csv_writer.writerow(modified_row)
        
    count += 1
    # if (count == 5):
    #     break

OUTPUT_FILE.close()
FILE.close()
