"""
Portfolio strategy instance
"""
from dataclasses import dataclass

from catcher_bot.model.config import Config


@dataclass(frozen=True)
class PortfolioConfig(Config):
    """
    Portfolio configs
    """
    def __post_init__(self):
        super().__init__(self.code, self.config_type, self.description, self.filepath)
