import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from common.consts import LOG_FILE_PATH, LOG_PATH

logger = logging.getLogger('default_logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")


def _add_log_handler(handler):
    handler.setFormatter(formatter)
    logger.addHandler(handler)


_add_log_handler(logging.StreamHandler(sys.stdout))
os.makedirs(LOG_PATH, exist_ok=True)
_add_log_handler(RotatingFileHandler(LOG_FILE_PATH, maxBytes=1024 * 1024 * 5, backupCount=10))


def debug(msg, **kwargs):
    logger.debug(msg + ' ' + ', '.join([f'{k}: {v}' for k, v in kwargs.items()]))
