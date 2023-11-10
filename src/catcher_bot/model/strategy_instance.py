"""
Strategy instance class
"""
from dataclasses import dataclass
from catcher_bot.model.strategy import Strategy


@dataclass(frozen=True)
class StrategyInstance:
    """
    Strategy code module with base parameters
    """
    module: type[Strategy]
    filepath: str
    name: str
    code: str
