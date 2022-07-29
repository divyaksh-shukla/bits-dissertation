import csv
from datetime import datetime, timedelta
from itertools import count
import json
import requests
from uuid import uuid4
from pprint import pprint

TOKEN_URL = 'https://idenserver.itrontotalstage.com/connect/token'
STAGE_CLIENT = {
    'client_id': '35875b30-0568-4e34-8c45-6662406ec0e6',
    'client_secret': 'frcstusr123',
    'grant_type': 'client_credentials',
    'scope': 'forecastingscope',
}

HEADERS = {
    'correlationId': str(uuid4()),
    'Itron-CorrelationId': str(uuid4()),
    'Content-Type': 'application/x-www-form-urlencoded',
}

DATA_URL = 'https://k8s.itrontotalstage.com/forecastadmingateway/api/v1/forecast/tenants/62434e0a-bf41-42c5-8a09-f7f7a15f0a6c/historical-view/chart'
DATA_HEADERS = {
    'Authorization': 'Bearer {}',
    'Itron-ClientId': '6c4b2dea2fff477ab641222a7860fb25',
    'Itron-TenantId': '35035eed9b394d1a8f2e3575b27d009e',
    'Itron-UserId': '99ae984bb03b435e9500c2e6518c4f76',
    'duration': '1',
    'endDate': '2022-07-28T23:59:59Z',
    'id': '23',
    'instanceName': 'Itron Demo',
    'languageCode': 'en-US',
    'startDate': '2022-06-28T00:00:00Z',
    'tenantId': '62434e0a-bf41-42c5-8a09-f7f7a15f0a6c',
    'type': 'Actual Load',
    'userId': '99ae984bb03b435e9500c2e6518c4f76',
    'weatherConceptKey': '0',
    'weatherKey': '1143',
}
DATA_HEADERS.update(HEADERS)

def write_to_file(filepath, data):
    _file = open(filepath, 'w')
    csv_writer = csv.writer(_file)
    count = 0
    for row in data:
        if (count == 0):
            csv_header = row.keys()
            csv_writer.writerow(csv_header)
            count += 1
        output_row = list(row.values())
        localdate = datetime.strptime(output_row[0], '%Y-%m-%dT%H:%M:%S+00:00') - timedelta(seconds=21600)
        output_row[0] = localdate.strftime('%Y-%m-%dT%H:%M:%S')
        csv_writer.writerow(output_row)
    _file.close()



response = requests.post(url=TOKEN_URL, headers=HEADERS, data=STAGE_CLIENT)

if (response.ok):
    auth_data = json.loads(response.text)
    token = auth_data['access_token']

    header = DATA_HEADERS
    header['Authorization'] = header['Authorization'].format(token)
    endDate = datetime.utcnow()
    startDate = endDate - timedelta(days = 365)
    header['startDate'] = startDate.strftime('%Y-%m-%dT00:00:00Z')
    header['endDate'] = endDate.strftime('%Y-%m-%dT23:59:59Z')
    pprint(f'StartDate: {header["startDate"]} | EndDate: {header["endDate"]}')
    data_response = requests.get(url=DATA_URL, headers=header)
    if(data_response.ok):
        data = data_response.json()
        write_to_file('houston_historical_load.csv', data['result']['historicalDataList'])

else :
    pprint('Token invalid')
    pprint(response.status_code)
    pprint(response.text)

