import logging
import logging.config
from pathlib import Path
import sys
import os


def initialise_logger(logging_ini_path):
    # load log file
    try:
        logging.config.fileConfig(logging_ini_path)
    except FileNotFoundError as fnf_error:
        logs_dir = Path(fnf_error.filename).parent
        Path(logs_dir).mkdir(exist_ok=True)
        logging.config.fileConfig(logging_ini_path)

    # log unhandled exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.critical(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback))

    # register system exception handler
    sys.excepthook = handle_exception
