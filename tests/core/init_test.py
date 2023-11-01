import pytest
from core import init

from tests.context import bc
from model.strategy import Strategy

# @pytest.mark.parametrize(("path"), [("strategies"), ("../strategies"),
#                                     (os.path.abspath(os.path.join(os.path.curdir, "../..", "strateies")))])
def test_init_strategies(bc):
    path = 'strategies'
    strategies = init.init_strategies(bc, path)
    assert strategies
    assert issubclass(strategies[0], Strategy)
