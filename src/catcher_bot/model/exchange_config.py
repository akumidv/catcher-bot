"""
Exchange config
"""
from dataclasses import dataclass

from catcher_bot.model.config import Config


@dataclass(frozen=True)
class ExchangeConfig(Config):
    """
    Exchange config class
    """
    exchange_code: str
    type: str
    symbols: list

    def __post_init__(self):
        super().__init__(self.code, self.config_type, self.description, self.filepath)
