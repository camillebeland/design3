from nose.tools import *
from unittest.mock import *
import base_station.logger as logger
from base_station.logger import Logger
import web_app

import logging


class TestLogging:

    def test_can_log_something_happening_on_robot(self):
        # Given
        web_app.run()

        # When


        # Then
        assert(True)



