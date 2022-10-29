import datetime
from typing import Optional, Union, Dict
import logging
import os
import sys

LOG_NAME = 'bot'
FORMAT_STR = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
DATE_FORMAT_STR = '%Y-%m-%d %H:%M:%S'
HANDLERS = []



def init(levels: Optional[Dict] = None):
    global HANDLERS
    HANDLERS = list()
    HANDLERS.extend(_get_handlers(levels))

    # console_handler = logging.StreamHandler(sys.stderr)
    # console_handler.setLevel(log_level)
    # HANDLERS.append(console_handler)
    # class LessThanFilter(logging.Filter):
    #     def __init__(self, exclusive_maximum, name=""):
    #         super(LessThanFilter, self).__init__(name)
    #         self.max_level = exclusive_maximum
    #
    #     def filter(self, record):
    #         # non-zero return means we log this message
    #         return 1 if record.levelno < self.max_level else 0
    # base_level = get_logger_type()
    # formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    # logging_handler_out = logging.StreamHandler(sys.stdout)
    # logging_handler_out.setLevel(logging.DEBUG)
    # logging_handler_out.addFilter(LessThanFilter(logging.WARNING))
    # logging_handler_out.setFormatter(formatter)
    # root_logger.addHandler(logging_handler_out)
    # logging_handler_err = logging.StreamHandler(sys.stderr)
    # logging_handler_err.setLevel(logging.WARNING)
    # logging_handler_err.setFormatter(formatter)
    # root_logger.addHandler(logging_handler_err)


def get_logger(module_name: Optional[str] = None):
    if len(HANDLERS) == 0:
        init()
    name = LOG_NAME
    if module_name is not None:
        name = f'{LOG_NAME}:{module_name}'
    logging.basicConfig(handlers=HANDLERS)
    module_logger = logging.getLogger(name)
    module_logger.handlers = HANDLERS

    return module_logger


def _get_logger_type(log_level=None, default='info'):
    all_log_levels = ['info', 'debug', 'warning', 'error', 'critical']
    if not isinstance(log_level, str) or log_level.lower() not in all_log_levels:
        log_level = default if isinstance(default, str) and default in all_log_levels else 'info'
    log_level = log_level.lower()
    if log_level == 'debug':
        return logging.DEBUG
    elif log_level == 'warning':
        return logging.WARNING
    elif log_level == 'error':
        return logging.ERROR
    elif log_level == 'critical':
        return logging.CRITICAL
    return logging.INFO


def _get_log_formatter() -> logging.Formatter:
    return logging.Formatter(fmt=FORMAT_STR, datefmt=DATE_FORMAT_STR)


def _get_handlers(levels: Optional[Dict] = None):

    handlers = []
    if levels is None or not isinstance(levels, dict):
        levels = {}
    cur_date = datetime.datetime.now()
    log_level = _get_logger_type(levels.get('console'), default=os.environ.get('LOG_LEVEL', 'info').lower())
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(_get_log_formatter())
    handlers.append(console_handler)

    if 'file' in levels:
        file_handler = logging.FileHandler(filename=f'bot_{cur_date.isoformat(timespec="minutes")}.log', mode='w',
                                           delay=True)  # RotatingFileHandler or TimedRotatingFileHandler may be better?
        log_level = _get_logger_type(levels['file'], default='debug')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(_get_log_formatter())
        handlers.append(file_handler)
    if 'messanger' in levels:
        raise NotImplementedError('Messanger as log did not implemented yet')
    return handlers

