"""
Strategy configuration class
"""
from dataclasses import dataclass, field

from catcher_bot.model.config import Config


@dataclass(frozen=True)
class StrategyConfig(Config):
    """
    Strategy configuration structure
    """
    parameters: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__init__(self.code, self.config_type, self.description, self.filepath)
    # exchanges_symbols: list[ExchangeConfig]

    # def __init__(self, code: str, parameters: dict = None): # exchanges_symbols: list[dict],
    #     self.code = code
    #     self.parameters = {} if parameters is None else parameters
    #     # if len(exchanges_symbols) == 0:
        #     raise ValueError(f'exchanges_symbols in strategy config {self.code} are empty')
        # self.exchanges_symbols = [ExchangeConfig(**exchange_cfg) for exchange_cfg in exchanges_symbols]
