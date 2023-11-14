#pylint: disable=C0111,protected-access
import pytest

from catcher_bot.model import namespace as ns


def test_get_by_id():
    assert ns.ModuleType['STRATEGY'] == ns.ModuleType.get_by_id('strategy')
    assert ns.ModuleType['PORTFOLIO'] == ns.ModuleType.get_by_id(ns.ModuleType['PORTFOLIO'].value)
    assert ns.ModuleType['CONNECTOR'] == ns.ModuleType.get_by_id(ns.ModuleType['CONNECTOR'])
    with pytest.raises(KeyError):
        _ = ns.ModuleType['WRONG_TYPE']
    with pytest.raises(KeyError):
        _ = ns.ModuleType.get_by_id('WRONG_TYPE')
    with pytest.raises(KeyError):
        _ = ns.ModuleType.get_by_id(-1)
