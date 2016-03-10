from nose.tools import *
from unittest.mock import *
from robot.robot_service import RobotService
import os
from configuration import configuration


def find_in_log_file(message):
    base_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    log_file_path = os.path.join(base_directory, 'system.log')

    with open(log_file_path) as open_file:
        lines = open_file.readlines()

    for line in lines:
        if message in line:
            return True

    return False;


def setup_function():
    print("setup")


def teardown_function():
    print("teardown")


@with_setup(setup_function, teardown_function)
def test_can_log_something_happening_on_robot():
    # Given
    config = configuration.get_config()
    base_station_host = config.get('baseapp', 'host')
    base_station_port = config.get('baseapp', 'port')
    base_station_address = "http://" + base_station_host + ":" + base_station_port
    robot_service = RobotService(base_station_address)

    message = "test_can_log_something_happening_on_robot!"

    # When
    robot_service.log_info(message)

    # Then
    message_is_in_log_file = find_in_log_file(message)
    assert(message_is_in_log_file)










