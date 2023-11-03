from dataclasses import dataclass, field
from model.strategy import Strategy
from model.strategy_config import StrategyConfig
from typing import List, Dict


@dataclass(frozen=True)
class StrategyInstance:
    module: Strategy
    filepath: str
    name: str
    code: str
    configs: List[StrategyConfig]
