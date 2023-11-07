from dataclasses import dataclass, field
from catcher_bot.model.strategy import Strategy
from catcher_bot.model.strategy_config import StrategyConfig
from typing import List, Dict


@dataclass(frozen=True)
class StrategyInstance: # TODO should be instance or have sence init in child process with data and control pipes?
    module: type[Strategy]
    filepath: str
    name: str
    code: str
    configs: list[StrategyConfig]
