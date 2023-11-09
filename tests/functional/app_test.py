#pylint: disable=C0111,protected-access
from catcher_bot import app
from catcher_bot.core.bot_context import BotContext


def test_init():
    bc = app.init()
    assert issubclass(bc, BotContext)
