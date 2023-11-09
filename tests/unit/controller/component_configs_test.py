#pylint: disable=C0111,protected-access
import pytest

from catcher_bot.core import component_configs


config_base = {
    'path': {'config': 'configs_example'}
}


def test_get_configs():
    component_configs.get_configs()

