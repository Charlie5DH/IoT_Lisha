import time
import requests
import json

get_url = 'https://iot.ufsc.br/api/get.php'

epoch = int(time.time() * 1000000)

query = {
    'series': {
        'version': '1.1',
        'unit': 2224179556,	# unit Temperature
        'x': 0,
        'y': 1,
        'z': 2,
        'r': 0,
        't0': epoch - (3 * 3600 * 1000000),     # 3 hours
        't1': epoch,							# now
        'dev': 0
    },
    'credentials': {
        'domain': 'tutorial',
        'username': 'tutorial',
        'password': 'tuto20182'
    }
}

session = requests.Session()
session.headers = {'Content-type': 'application/json'}
response = session.post(get_url, json.dumps(query))

print("Get [", str(response.status_code), "] (")
print(json.dumps(query, indent=4))
if response.status_code == 200:
    data = response.json()
    print(type(data))
    print(json.dumps(data, indent=4))






