from dataclasses import dataclass, field
import yaml


@dataclass(frozen=False)
class StrategyConfig:
    name: str
    parameters: dict = field(default_factory=dict)

    def to_yaml(self) -> str:
        config_dict = {}
        for field_name in self.__dataclass_fields__:
            config_dict[field_name] = getattr(self, field_name)
        return yaml.dump(config_dict)


def get_empty_strategy_config(strategy_code: str) -> StrategyConfig:
    return StrategyConfig(name=strategy_code)
