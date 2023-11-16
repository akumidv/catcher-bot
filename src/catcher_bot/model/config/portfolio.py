"""
Portfolio strategy instance
"""
from dataclasses import dataclass

from catcher_bot.model.config.base import BaseConfig


# TODO test
# TODO parsing for timeframes, expirations, option strikes, symbold, exchanges

@dataclass(frozen=False)
class PortfolioConfig(BaseConfig):
    """
    Portfolio configs
    """
    def __post_init__(self):
        super().__init__(self.code, self.config_type, self.description, self.filepath)
