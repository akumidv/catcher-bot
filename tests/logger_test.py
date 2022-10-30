"""
WARNING. To show log in pycharm set additional arguments to "-s -o log_cli=true  -o log_cli_level=DEBUG"
"""
import os

import logger
import logging


def test_get_logger():
    logger.init({'file': 'debug', 'console': 'info'})
    test_phrase = ['value', 'qwerty']
    for idx in range(2):
        log = logger.get_logger(module_name=f'test_{idx}')
        log.debug(f'{test_phrase[0]}_{idx}')
        log.warn(f'{test_phrase[1]}_{idx}')
    file_handler_idx = [i for i in range(len(log.handlers)) if repr(log.handlers[i]).startswith('<FileHandler')]
    assert len(file_handler_idx)
    log_fn = repr(log.handlers[file_handler_idx[0]]).replace('<FileHandler ', '')
    log_fn = log_fn[:log_fn.find('.log') + 4]
    with open(log_fn, 'r') as fl:
        file_contents = fl.read()
    os.remove(log_fn)
    print('Log file', log_fn, 'contain:')
    print(file_contents)
    assert '[DEBUG' in file_contents and '[WARNING' in file_contents
    assert 'test_0' in file_contents and 'value_0' in file_contents
    assert 'test_1' in file_contents and 'qwerty_1' in file_contents


def test_init():
    logger.init({'console': 'warning'})
    assert len(logger.HANDLERS) == 1
    assert isinstance(logger.HANDLERS[0], logging.StreamHandler)
    logger.init()
    assert len(logger.HANDLERS) == 2
    assert isinstance(logger.HANDLERS[0], logging.StreamHandler)
    assert isinstance(logger.HANDLERS[1], logging.StreamHandler)
    logger.init({'file': 'debug'})
    assert len(logger.HANDLERS) == 3
    assert isinstance(logger.HANDLERS[2], logging.FileHandler)


def test__get_logger_type():
    log_level = logger._get_logger_type('warning')
    assert log_level == logging.WARNING
    log_level = logger._get_logger_type()
    assert log_level == logging.INFO
    log_level = logger._get_logger_type(12)
    assert log_level == logging.INFO
    log_level = logger._get_logger_type(12, 'debug')
    assert log_level == logging.DEBUG

