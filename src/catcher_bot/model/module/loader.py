"""
Base instance class for module loading form path that set by user
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleLoader:
    """
    Base module
    """
    class_instance: type
    code: str
    filepath: str
