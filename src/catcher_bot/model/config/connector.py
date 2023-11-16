"""
Exchange config
"""
from dataclasses import dataclass, field

from catcher_bot.model.config.base import BaseConfig
from catcher_bot.model.namespace import MarketType, ConnectorType, InstrumentType


@dataclass(frozen=False)
class ConnectorConfig(BaseConfig):
    """
    Exchange config class
    """
    connector_code: str
    # connector_type: str # TODO They are set in connector, do it really need?
    # market_type: str # TODO They are set in connector, do it really need?
    # instrument_type: str # TODO They are set in connector, do it really need?
    credentials: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__init__(self.code, self.config_type, self.description, self.filepath)
        # if not ConnectorType.is_valid_name(self.connector_type):
        #     raise ValueError(f"{self.connector_type} value is not correct for connector_type")
        # if MarketType.is_valid_name(self.market_type):
        #     raise ValueError(f"{self.market_type} value is not correct for market_type")
        # if InstrumentType.is_valid_name(self.instrument_type):
        #     raise ValueError(f"{self.instrument_type} value is not correct for instrument_type")
