"""
Base instance class for module laoding form path that set by user
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
