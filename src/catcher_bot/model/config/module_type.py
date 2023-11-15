from typing import Hashable, Callable, Union

from catcher_bot.model.namespace import ModuleType
from catcher_bot.model.config.strategy import StrategyConfig
from catcher_bot.model.config.portfolio import PortfolioConfig
from catcher_bot.model.config.connector import ConnectorConfig

CONFIG_CLASSES: dict[Union[Hashable, int], Callable[..., object]] = {
    ModuleType.STRATEGY: StrategyConfig,
    ModuleType.PORTFOLIO: PortfolioConfig,
    ModuleType.CONNECTOR: ConnectorConfig
}
