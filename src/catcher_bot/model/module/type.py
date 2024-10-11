from typing import Hashable, Callable, Union

from catcher_bot.model.namespace import ModuleType
from catcher_bot.model.module.strategy import Strategy
from catcher_bot.model.module.portfolio import Portfolio
from provider.connector import Connector

MODULE_CLASSES: dict[Union[Hashable, int], Callable[..., object]] = {
    ModuleType.STRATEGY: Strategy,
    ModuleType.PORTFOLIO: Portfolio,
    ModuleType.CONNECTOR: Connector
}
