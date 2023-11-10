"""
Base class of configs
"""
from dataclasses import dataclass, asdict

import yaml


@dataclass(frozen=True)
class Config:
    """
    Base Config class
    """
    code: str
    config_type: str
    description: str
    filepath: str

    def to_yaml(self) -> str:
        """
        Converting configuration to yaml
        """
        config_dict = asdict(self)
        if 'filepath' in config_dict:
            del config_dict['filepath']
        return yaml.dump(config_dict)
