"""
Bot logger
"""

import datetime
from typing import Optional, Dict
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler #, RotatingFileHandler


LOG_NAME: str = 'bot'
FORMAT_STR: str = '%(asctime)s [%(levelname)-7s] %(name)10s: %(message)s'
FORMAT_STR_ERROR: str = '%(asctime)s [%(levelname)-7s] %(name)10s %(filename)s:%(funcName)s:%(lineno)-3d: %(message)s'
FORMAT_STR_FILE: str = '%(asctime)s [%(levelname)-7s] %(name)10s %(filename)s:%(lineno)-3d: %(message)s'
DATE_FORMAT_STR: str = '%Y-%m-%d %H:%M:%S'
HANDLERS: list = []
MIN_LEVEL: int = logging.INFO

LOG_FOLDER: str = os.path.abspath(os.path.join(os.path.curdir, 'log')) # TODO to config


def get_def_logger(name):
    """
    Preparing bot logger
    """
    return logging.getLogger(name)


def _init(levels: Optional[Dict] = None):
    """
    Initializing bol logger
    """
    global HANDLERS
    global MIN_LEVEL
    HANDLERS = []
    handlers, set_level = _get_handlers_and_min_level(levels)
    HANDLERS.extend(handlers)
    if set_level is not None:
        MIN_LEVEL = set_level


def get_logger(module_name: Optional[str] = None, init_levels: Optional[Dict] = None) -> logging.Logger:
    """
    Get logger with current configurations
    """
    if len(HANDLERS) == 0:
        _init(init_levels)
    name = LOG_NAME
    if module_name is not None:
        name = f'{LOG_NAME}:{module_name}'
    # logging.basicConfig(level=MIN_LEVEL,  handlers=HANDLERS) #handlers=[]) #, handlers=HANDLERS)
    module_logger = logging.getLogger(name)
    module_logger.setLevel(MIN_LEVEL)
    #module_logger.handlers = HANDLERS
    for handler in HANDLERS:
        module_logger.addHandler(handler)
    return module_logger


def _get_logger_type(log_level_name=None, default='warning'):
    all_log_levels = ['info', 'debug', 'warning', 'error', 'critical']
    if not isinstance(log_level_name, str) or log_level_name.lower() not in all_log_levels:
        log_level_name = default if isinstance(default, str) and default in all_log_levels else 'warning'
    log_level_name = log_level_name.lower()
    log_level = logging.INFO
    if log_level_name == 'debug':
        log_level = logging.DEBUG
    elif log_level_name == 'warning':
        log_level = logging.WARNING
    elif log_level_name == 'error':
        log_level = logging.ERROR
    elif log_level_name == 'critical':
        log_level = logging.CRITICAL
    return log_level


def _get_log_formatter(fmt=FORMAT_STR_ERROR) -> logging.Formatter:
    return logging.Formatter(fmt=fmt, datefmt=DATE_FORMAT_STR)


class LevelFilter(logging.Filter):
    """
    Filtering for levels
    """
    def __init__(self, level, name=""):
        super(LevelFilter, self).__init__(name)
        self.level = level

    def filter(self, record):  # non-zero return means we log this message
        return True if record.levelno < self.level else False # TODO fix and test


def _get_handlers_and_min_level(levels: Optional[Dict] = None):
    handlers = []
    if levels is None or not isinstance(levels, dict):
        levels = {'console': 'info'}
    cur_date = datetime.datetime.now(tz=datetime.timezone.utc)
    set_level = None
    if 'console' in levels:
        log_level = _get_logger_type(levels.get('console'), default=os.environ.get('LOG_LEVEL', 'info').lower())
        set_level = log_level
        console_err_handler = logging.StreamHandler(sys.stderr)
        console_err_handler.setLevel(log_level if log_level > logging.WARNING else logging.WARNING)
        console_err_handler.setFormatter(_get_log_formatter(FORMAT_STR_ERROR))
        handlers.append(console_err_handler)
        if log_level < logging.WARNING:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(_get_log_formatter(FORMAT_STR))
            console_handler.addFilter(LevelFilter(logging.WARNING))
            handlers.append(console_handler)

    if 'file' in levels:
        os.makedirs(LOG_FOLDER, exist_ok=True) # TODO name and parameters to config
        log_fn = f'{LOG_FOLDER}/bot_{cur_date.isoformat(timespec="minutes")}.log'
        # file_handler = logging.FileHandler(filename=filename, mode='w', delay=True)  # RotatingFileHandler or TimedRotatingFileHandler may be better?
        # file_handler = RotatingFileHandler(filename=log_fn, maxBytes=100000, backupCount=10, delay=True)
        file_handler = TimedRotatingFileHandler(filename=log_fn, when='D', interval=1, backupCount=14, delay=True)
        log_level = _get_logger_type(levels['file'])
        if set_level is None or set_level > log_level:
            set_level = log_level
        file_handler.setLevel(log_level)
        file_handler.setFormatter(_get_log_formatter(FORMAT_STR_FILE))
        handlers.append(file_handler)
    if 'messanger' in levels:
        raise NotImplementedError('Messanger as log did not implemented yet')
    return handlers, set_level
