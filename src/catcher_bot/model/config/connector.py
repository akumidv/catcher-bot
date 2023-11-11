"""
Exchange config
"""
from dataclasses import dataclass

from catcher_bot.model.config.base import BaseConfig


# TODO test
# TODO different connectors - exchanges, providers, source files


@dataclass(frozen=True)
class ConnectorConfig(BaseConfig):
    """
    Exchange config class
    """
    connector_code: str
    type: str
    symbols: list

    def __post_init__(self):
        super().__init__(self.code, self.config_type, self.description, self.filepath)
