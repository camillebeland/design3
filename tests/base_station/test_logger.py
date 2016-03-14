from nose.tools import *
from unittest.mock import *
import base_station.logger as logger
from base_station.logger import Logger

import logging


class TestBaseStationWebController:

    def test_warning_should_send_message_to_real_logging(self):
        # Given
        a_message = "Something is weird"
        logger = Logger()
        mock_logging = Mock()
        logger.inject_mock_logging(mock_logging)

        # When
        logger.warning(a_message)

        # Then
        mock_logging.warning.assert_called_once_with(a_message)


    def test_warning_should_send_message_to_real_logging(self):
        # Given a mocked logging
        a_message = "Something has happened during the normal course of the system"
        logger = Logger()
        mock_logging = Mock()
        logger.inject_mock_logging(mock_logging)

        # When
        logger.info(a_message)

        # Then
        mock_logging.info.assert_called_once_with(a_message)

