"""
Base module instance class
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Module:
    """
    Base module
    """
    class_instance: type
    code: str
    filepath: str
