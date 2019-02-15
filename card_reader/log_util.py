import logging
from logging.config import fileConfig


def get_logger():
    fileConfig('logging_config.ini')
    logger = logging.getLogger()
    return logger