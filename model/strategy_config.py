from dataclasses import dataclass, field, asdict, InitVar
import yaml


@dataclass(frozen=True)
class ExchangeConfig:
    exchange_code: str
    type: str
    symbols: list


@dataclass(frozen=False)
class StrategyConfig:
    code: str
    exchanges_symbols: list[ExchangeConfig]
    parameters: dict = field(default_factory=dict)

    def __init__(self, code: str, exchanges_symbols: list[dict], parameters: dict = None):
        self.code = code
        self.parameters = dict() if parameters is None else parameters
        if len(exchanges_symbols) == 0:
            raise ValueError(f'exchanges_symbols in strategy config {self.code} is empty')
        # if isinstance(self.exchanges_symbols, dict):
        self.exchanges_symbols = [ExchangeConfig(**exchange_cfg) for exchange_cfg in exchanges_symbols]


    def to_yaml(self) -> str:
        return yaml.dump(asdict(self))


# TODO depricated? or get exchanges and types from bot config?
def get_empty_strategy_config(strategy_code: str) -> StrategyConfig:
    return StrategyConfig(code=strategy_code, exchanges_symbols=[{'exchange_code': 'binance', "type": "futures", "symbols": ['BTCUSDT']}], parameters=dict())
