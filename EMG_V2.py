#!/usr/bin/env python3
# https://iot.lisha.ufsc.br:3000/invite/v6wx1EI08vrFOoHT25Nte1Wx6R1aZ6 grafana user
# https://iot.lisha.ufsc.br:3000/d/EX1S3eZZz/carlos?tab=visualization&orgId=1&from=now&to=now%2B10m&refresh=5s

import time
import requests
import json
from enum import IntEnum
from sense_hat import SenseHat
import serial
import smtplib
import ssl
import numpy

sense = SenseHat()
device = '/dev/ttyACM0'
arduinoCom = serial.Serial(device, 115200)
arduinoCom.baudrate = 115200

sense = SenseHat()
SMTP_SERVER = "smtp.gmail.com"
PORT = 465  # For SSL
SENDER_EMAIL = "raspberrypi.iot.lisha@gmail.com"
SENDER_PASSWORD = ""
RECEIVER_EMAIL = ""
ATTACH_URL = "https://iot.lisha.ufsc.br/api/attach.php"
PUT_URL = "https://iot.lisha.ufsc.br/api/put.php"
GET_URL = "https://iot.ufsc.br/api/get.php"
USERNAME = "tutorial"
DOMAIN = "tutorial"
PASSWORD = "tuto20182"
CERTIFICATE = "PATH_TO_CERTIFICATE_FILE"
SIMULATION_TIME = 20    # seconds
INTERVAL = 2*1000000    # useconds

t0 = int(time.time() * 1000000)         # Current time
t1 = t0 + SIMULATION_TIME * 1000000     # time limit (*1000000 for adding precision)
x = 0                                   # x,y,z coordinates from the device
y = 1
z = 2
r = 0                                   # in a radius
dev = 0                                 # device (always the same in this case)
error = 0                               # no error in measure
conf = 1                                # 100% trust in the value

session = requests.Session()
session.headers = {'Content-type': 'application/json'}


class Unit(IntEnum):
    TEMPERATURE = 2224179556
    PRESSURE = 2223941924
    ACCELERATION = 2224433444
    VOLTAGE = 2224723748


def rest_send(data, url):
    try:
        response = session.post(url, json.dumps(data))

        # print("[", str(response.status_code), "] (")
    except Exception as e:  # catches exceptions of type Exception.The exception rised(object)is bounded to e
        print("Exception caught:", e)


def rest_get(get_url, query):
    try:
        response = session.post(get_url, json.dumps(query))

        # print("[", str(response.status_code), "] (")
    except Exception as e:  # catches exceptions of type Exception.The exception rised(object)is bounded to e
        print("Exception caught:", e)
    return response


def send_series(unit):  # function to to transform the unit to JSON format(create series)
    ret_obj = {
        'series':
            {
                'version': "1.1",  # version of the test
                'unit': unit.value,  # code of the measured unit
                'x': x,  # x coordinate
                'y': y,  # Y coordinate
                'z': z,  # Z coordinate
                'r': r,  # radius
                't0': t0,  # initial time
                't1': t1,  # final time
                'dev': dev,  # device
                'workflow': 0
            },
        'credentials':
            {
                'domain': DOMAIN,
                'username': USERNAME,
                'password': PASSWORD
            }
    }
    rest_send(ret_obj, ATTACH_URL)


def send_data(data, unit, time_stamp):  # function to transform the the smartdata to JSON format
    ret_obj = {
        'smartdata': [
            {
                'version': '1.1',
                'unit': unit.value,
                'value': data,
                'error': error,
                'confidence': conf,
                'x': x,
                'y': y,
                'z': z,
                't': time_stamp,
                'dev': dev,
                'workflow': 0
            }
        ],
        'credentials': {
            'domain': DOMAIN,
            'username': USERNAME,
            'password': PASSWORD
        }
    }
    rest_send(ret_obj, PUT_URL)


def query_data(unit, begin, end):
    query = {
        'series': {
            'version': '1.1',
            'unit': unit,
            'x': x,
            'y': y,
            'z': z,
            'r': r,
            't0': begin,
            't1': end,
            'dev': dev
        },
        'credentials': {
            'domain': DOMAIN,
            'username': USERNAME,
            'password': PASSWORD
        }
    }
    return rest_get(GET_URL, query)


send_series(Unit.VOLTAGE)

beg = t0
end = t0 + INTERVAL
start = 0
i = 0
j = 0
FLAG = 1
values = []
timestamp = []
counter = 0

# EMG_file = open('EMG_file.dat', 'wb')
# header = "Voltage, Time\n"
# np.savetxt('EMG_file.dat', [], header=header)

while start <= t1:
    start = time.time() * 1000000
    voltage = float(arduinoCom.readline())
    if voltage >= 0.0001:
        send_data(voltage, Unit.VOLTAGE, (int((time.time() * 1000000))))
        print(voltage)

while beg < t1:
    response = query_data(Unit.VOLTAGE, beg, end)
    query = response.json()
    while i < len(query["series"]):
        if query["series"][i]["value"] < 1.9:
            values.append(query["series"][i]["value"])
            timestamp.append(query["series"][i]["timestamp"])
            FLAG = 0
        i += 1
    if FLAG == 1:
        counter = counter +1
    i = 0
    beg = end
    end = end + INTERVAL

end_time = str(time.localtime(time.time()))

MESSAGE = """\
Subject: Hi there

This message was send using Python3 from a Raspberry Pi
from the LISHA department at UFSC.
The experiment finished at
""" + end_time + """
 This is simply to remind you that the electromyogram has finished
and the results shows that were """ + str(counter) + """.
 Phasic events. You can go to https://iot.ufsc.br/HomePage to see the results
Bye Bye"""


# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, MESSAGE)
