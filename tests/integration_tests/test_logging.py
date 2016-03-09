from nose.tools import *
from unittest.mock import *
import base_station.logger as logger
from base_station.logger import Logger
import base_station_app
from base_station.base_station_web_controller import app


def setup_function():
    base_station_app.run()
    #print("bob")

def teardown_function():
    "tear down test fixtures"


@with_setup(setup_function, teardown_function)
def test_can_log_something_happening_on_robot():
    # Given


    # When


    # Then
    assert(True)










