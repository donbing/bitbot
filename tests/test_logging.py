import unittest
import logging
from src.configuration.bitbot_logging import initialise_logger
from os import path

class TestLogging(unittest.TestCase):
    display_size = (400, 300)

    def test_logging_something(self):
        current_path = path.dirname(path.abspath(__file__))
        log_file_path = path.join(current_path, '../config/logging.ini')
        initialise_logger(log_file_path)
        logging.debug('log test')
