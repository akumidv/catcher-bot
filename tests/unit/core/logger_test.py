#pylint: disable=C0111,protected-access
"""
WARNING. To show log in pycharm set additional arguments to "-s -o log_cli=true  -o log_cli_level=DEBUG"
"""
import os
import logging
from catcher_bot.core import logger


def test_show_logger_lev(caplog):
    logger._init({'console': 'debug'})
    log = logger.get_logger(module_name='test_log')
    with caplog.at_level(logging.DEBUG):
        log.debug("Debug[TEST]")
    assert "Debug[TEST]" in caplog.text
    with caplog.at_level(logging.INFO):
        log.info("Info[TEST]")
    assert "Info[TEST]" in caplog.text
    with caplog.at_level(logging.WARNING):
        log.warning("Warning[TEST]")
    assert "Warning[TEST]" in caplog.text
    with caplog.at_level(logging.ERROR):
        log.error("Error[TEST]")
    assert "Error[TEST]" in caplog.text
    with caplog.at_level(logging.CRITICAL):
        log.critical("Critical[TEST]")
    assert "Critical[TEST]" in caplog.text


def test_get_logger(caplog):
    logger._init({'file': 'debug', 'console': 'info'})
    test_phrase = ['value', 'qwerty']
    caplog.set_level(logging.DEBUG)

    for idx in range(2):
        log = logger.get_logger(module_name=f'test_{idx}')
        log.debug(f"{test_phrase[0]}_{idx}")
        log.warning(f"{test_phrase[1]}_{idx}")
    assert f"{test_phrase[0]}_0" in caplog.text
    assert f"{test_phrase[0]}_1" in caplog.text
    assert f"{test_phrase[1]}_0" in caplog.text
    assert f"{test_phrase[1]}_1" in caplog.text

    file_handler_idx = [i for i in range(len(log.handlers)) \
                            if repr(log.handlers[i]).startswith('<FileHandler') or \
                               repr(log.handlers[i]).startswith('<TimedRotatingFileHandler') or \
                               repr(log.handlers[i]).startswith('<RotatingFileHandler')]
    assert len(file_handler_idx)

    log_fn = repr(log.handlers[file_handler_idx[0]]).replace('<FileHandler ', '')\
                                                    .replace('<TimedRotatingFileHandler ', '')\
                                                    .replace('<RotatingFileHandler ', '')
    log_fn = log_fn[:log_fn.find('.log') + 4]
    with open(log_fn, 'r', encoding='utf-8') as fl:
        file_contents = fl.read()
    os.remove(log_fn)
    print('Log file', log_fn, 'contain:')
    print(file_contents)
    assert '[DEBUG' in file_contents and '[WARNING' in file_contents
    assert f"{test_phrase[0]}_0" in file_contents and f"{test_phrase[0]}_1" in file_contents
    assert f"{test_phrase[1]}_0" in file_contents and f"{test_phrase[1]}_1"  in file_contents


def test_init():
    logger._init({'console': 'warning'})
    assert len(logger.HANDLERS) == 1
    assert isinstance(logger.HANDLERS[0], logging.StreamHandler)
    logger._init()
    assert len(logger.HANDLERS) == 2
    assert isinstance(logger.HANDLERS[0], logging.StreamHandler)
    assert isinstance(logger.HANDLERS[1], logging.StreamHandler)
    logger._init({'file': 'debug'})
    assert len(logger.HANDLERS) == 1
    assert isinstance(logger.HANDLERS[0], logging.FileHandler)


def test__get_logger_type():
    assert logging.WARNING == logger._get_logger_type('warning')
    assert logging.WARNING == logger._get_logger_type()
    assert logging.WARNING == logger._get_logger_type(12)
    assert logging.DEBUG == logger._get_logger_type(12, 'debug')
