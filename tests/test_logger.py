from nose.tools import *
from unittest.mock import *
import base_station.logger as logger
from base_station.logger import warning
import logging


class TestBaseStationWebController():

    @patch('base_station.base_station_web_controller.logger.logging')
    def test_warning_should_send_message_to_real_logging(self, mock_logging):
        # Given a mocked logging
        a_message = "Something is weird"

        # When
        logger.warning(a_message)

        # Then
        mock_logging.warning.assert_called_once_with(a_message)


    @patch('base_station.base_station_web_controller.logger.logging')
    def test_warning_should_send_message_to_real_logging(self, mock_logging):
        # Given a mocked logging
        a_message = "Something has happened during the normal course of the system"

        # When
        logger.info(a_message)

        # Then
        mock_logging.info.assert_called_once_with(a_message)

