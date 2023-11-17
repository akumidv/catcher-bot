#pylint: disable=C0111,protected-access
import sys
from catcher_bot import app
from catcher_bot.model.bot_context import BotContext
from tests.conftest import WORKING_FOLDER, CONFIGS_FOLDER, CONFIG_BOT_FN

def test_init():
    sys.argv = ['app.py', '--cfg', f"{WORKING_FOLDER}/{CONFIG_BOT_FN}"]
    bc = app.init()
    assert isinstance(bc, BotContext)
