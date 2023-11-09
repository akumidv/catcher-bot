import pytest
import os
from catcher_bot.core.bot_context import BotContext
from catcher_bot.core.bot_config import _verify_config

#MOCKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))
WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))
CONFIG_PATH = 'mock_bot_config.yaml'

@pytest.fixture()
def bot_cfg():
    test_bot_cfg = {
    # exchanges=['binance'],
    # market_types=['futures'],
    # logger = {'console': 'debug'},
# telegram:
#   chat_id: ''
#   bot_token: ''
#     credentials = {
  #stock:
   # binance:
    #  api_key: ''
     # secret_key: ''
     #    'futures': {'binance': {'api_key': '', 'secret_key': ''}}
    # },
    # strategies = {'path': 'strategies'}
    'path': {'config': 'config_examples'}
    }
    return test_bot_cfg


@pytest.fixture()
def bc() -> BotContext:
    _verify_config(test_bot_cfg)
    bot_context = BotContext(test_bot_cfg)
    return bot_context