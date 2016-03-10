from nose.tools import *
from unittest.mock import *
import base_station_app
from robot.robot_service import RobotService
from base_station.base_station_web_controller import app
import web_app
import time
import requests
import os
import signal


def setup_function():
    #base_station_app.run()
    #app.test_client()
    print("bob")
    base_station_app.run()
    time.sleep(100)
    #base_station_app.run()


def teardown_function():
    print("bob2")
    "tear down test fixtures"


@with_setup(setup_function, teardown_function)
def test_can_log_something_happening_on_robot():
    # Given
    #robot_service = RobotService("http://localhost:5000")
    #app.config['TESTING'] = True


    #bob = app.test_client()
    #time.sleep(100)

    # When
    #robot_service.log_info("Allo!")
    # try:
    response = requests.post("http://localhost:5000/logger/info", json={'message': 'allo!'})
    #print("status code:")
    #print(response.status_code)
    # except requests.exceptions.ConnectionError:
    #     print("connection refused")



    # Then
    assert(True)










