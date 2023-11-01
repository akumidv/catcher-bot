from core.bot_context import BotContext
from core.config import _verify_config
import pytest

test_bot_cfg = dict(
    exchanges=['binance'],
    market_types=['futures'],
    logger = {'console': 'debug'},
# telegram:
#   chat_id: ''
#   bot_token: ''
    credentials = {
  #stock:
   # binance:
    #  api_key: ''
     # secret_key: ''
        'futures': {'binance': {'api_key': '', 'secret_key': ''}}
    },
    strategies = {'path': 'strategies'}
)


@pytest.fixture()
def bc() -> BotContext:
    _verify_config(test_bot_cfg)
    bcontext = BotContext(test_bot_cfg)
    return bcontext