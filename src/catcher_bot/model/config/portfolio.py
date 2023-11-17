"""
Portfolio strategy instance
"""
from dataclasses import dataclass, asdict
import yaml

from catcher_bot.model.config.base import BaseConfig


# TODO test
# TODO parsing for timeframes, expirations, option strikes, symbold, exchanges


@dataclass(frozen=False)
class SourceConfig:
    """
    Source config
    """
    connector_config_code: str
    assets: list
    common: dict | None = None
    black_list: list | None = None


@dataclass(frozen=False)
class ActionConfig:
    """
    Source config
    """
    connector_config_code: str


@dataclass(frozen=False)
class CompositionConfig:
    """
    Portfolio composition
    """
    strategy_config_code: str
    ratio: float
    sources: list[dict | SourceConfig]
    actions: list[dict | ActionConfig]

    def __post_init__(self):
        self.sources = [SourceConfig(**source_cfg) for source_cfg in self.sources]
        self.actions = [ActionConfig(**action_cfg) for action_cfg in self.actions]



@dataclass(frozen=False)
class PortfolioConfig(BaseConfig):
    """
    Portfolio configs
    """

    composition: list[dict | CompositionConfig]

    def __post_init__(self):
        super().__init__(self.code, self.config_type, self.description, self.filepath)
        self.composition = [CompositionConfig(**composition_cfg) for composition_cfg in self.composition]



