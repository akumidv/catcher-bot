#pylint: disable=C0111,protected-access,redefined-outer-name
import os
import pytest
import yaml

from catcher_bot.model.bot_context import BotContext
from catcher_bot.core.bot_configurator import _verify_config
from catcher_bot.core.component_configs import ComponentConfigs


WORKING_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))
STRATEGY_FOLDER = 'strategies'
CONFIGS_FOLDER = 'configs'
CONFIG_BOT_FN = 'mock_bot_config.yaml'
CONFIG_STRATEGY_FN = 'strategies/mock.yaml'
CONFIG_STRATEGY_FUT_FN = 'strategies/mock_futures.yaml'
CONFIG_PORTFOLIO_FN = 'portfolio/mock_portfolio_risk.yaml'
CONFIG_CONNECTOR_STOCK_FN = 'portfolio/mock_binance_stock.yaml'
CONFIG_CONNECTORS_DEREVIATEVE_FN = 'portfolio/mock_binance_derivatives.yaml'
STRATEGY_FN = 'mock_strategy.py'



_test_bot_cfg = {
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
    'path': {'config': CONFIGS_FOLDER,
             '__working_dir': WORKING_FOLDER},

}


@pytest.fixture()
def bot_config() -> dict:
    return _test_bot_cfg.copy()


@pytest.fixture()
def comp_strategy_config() -> dict:
    with open(os.path.join(WORKING_FOLDER, CONFIGS_FOLDER, CONFIG_STRATEGY_FN), 'r', encoding='utf-8') as fd:
        cfg = yaml.safe_load(fd)
    return cfg


@pytest.fixture()
def comp_configs(comp_strategy_config) -> ComponentConfigs:
    comp_cfg = ComponentConfigs(strategy={f"{comp_strategy_config['code']}": comp_strategy_config},
                                portfolio={}, exchange={})
    return comp_cfg


@pytest.fixture()
def b_context(bot_config, comp_configs) -> BotContext:
    _verify_config(bot_config)
    bot_context = BotContext(bot_config, comp_configs)
    return bot_context
