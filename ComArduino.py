#!/usr/bin/env python3
# https://iot.lisha.ufsc.br:3000/invite/v6wx1EI08vrFOoHT25Nte1Wx6R1aZ6 grafana user
# https://iot.lisha.ufsc.br:3000/d/EX1S3eZZz/carlos?tab=visualization&orgId=1&from=now&to=now%2B10m&refresh=5s

import os
import time
import requests
import json
import enum
from enum import IntEnum

import RPi.GPIO as GPIO
import serial
from sense_hat import SenseHat

sense = SenseHat()
device = '/dev/ttyACM0'
arduinoCom = serial.Serial(device, 9600)
arduinoCom.baudrate = 9600

ATTACH_URL = "https://iot.lisha.ufsc.br/api/attach.php"
PUT_URL = "https://iot.lisha.ufsc.br/api/put.php"
USERNAME = "tutorial"
DOMAIN = "tutorial"
PASSWORD = "tuto20182"
CERTIFICATE = "PATH_TO_CERTIFICATE_FILE"
SIMULATION_TIME = 60  # seconds

t0 = int(time.time() * 1000000)         # - 3600*1000000 # remind brt is -3hours from GMT.
t1 = t0 + SIMULATION_TIME * 1000000     # time limit (*1000000 for adding precision)
x = 0                                   # x,y,z coordinates from the device
y = 1
z = 2
r = 0                                   # in a radius
dev = 0                                 # device (always the same in this case)
error = 0                               # no error in measure
conf = 1                                # 100% trust in the value


class Unit(IntEnum):
    TEMPERATURE = 2224179556
    PRESSURE = 2223941924
    ACCELERATION = 2224433444
    VOLTAGE = 2224723748


def rest_send(data, url):
    session = requests.Session()
    session.headers = {
        'Content-type': 'application/json'}  # .headers returns a dictionary-like object, allowing access header
    # values by key. Indicates that the request body format is JSON.
    # session.cert = MY_CERTIFICATE

    try:  # .post to send JSON data through the message body.
        response = session.post(url, json.dumps(
            data))  # json.dumps(data) serialize data to JSON format.returns dictionary with indent
        # Post serialized data to url and save response
        # response is an object of type Response. Has the content of the web page

        # print("[", str(response.status_code), "] (", len(data), ") ", data)
    except Exception as e:  # catches exceptions of type Exception.The exception rised(object)is bounded to e
        print("Exception caught:", e)


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


send_series(Unit.TEMPERATURE)
# print("time t0 = ", time.localtime(t0 / 1000000))
# print("time t1 = ", time.localtime(t1 / 1000000))

if arduinoCom.inWaiting() > 0:
    response = arduinoCom.readline()
    if response == b'start\r\n':
        while True:
            if arduinoCom.inWaiting() > 0:
                number = ord(arduinoCom.read())
                if number == 100:
                    temperature = sense.get_temperature()
                    temperature = round(temperature, 2)
                    send_data(temperature, Unit.TEMPERATURE, (int((time.time() * 1000000))))
                    print(temperature)
                    print(number)
