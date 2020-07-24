import time
import requests
import json

get_url = 'https://iot.ufsc.br/api/get.php'

epoch = int(time.time() * 1000000)

query = {
    'series': {
        'version': '1.1',
        'unit': 2224179556,
        'x': 0,
        'y': 1,
        'z': 2,
        'r': 0,
        't0': epoch - (3 * 3600 * 1000000),     # 3 hours
        't1': epoch,
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
    print('\n')
    print(len(data["series"]))
    print('\n')
    i = 0
    j = 0
    values = []
    Count = 0

    while i < len(data["series"]):
        values.append(data["series"][i]["value"])
        i += 1
    print(values)

    while j < len(values):
        if values[j] > 29:
            Count += 1
        j += 1
    print('\n', Count)





