
from catcher_bot.model import namespace as ns
from catcher_bot.model.config.module_type import CONFIG_CLASSES

from catcher_bot.model.config.strategy import StrategyConfig
from catcher_bot.model.config.portfolio import PortfolioConfig
from catcher_bot.model.config.connector import ConnectorConfig


def test_config_classes_strategy():
    assert issubclass(CONFIG_CLASSES.get(ns.ModuleType.STRATEGY), StrategyConfig)


def test_config_classes_portfolio():
    assert issubclass(CONFIG_CLASSES.get(ns.ModuleType.PORTFOLIO), PortfolioConfig)


def test_config_classes_connect():
    assert issubclass(CONFIG_CLASSES.get(ns.ModuleType.CONNECTOR), ConnectorConfig)
