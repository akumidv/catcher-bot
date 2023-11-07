import logging

import pandas as pd
import pytest
from catcher_bot.interface.exchange.binance_class import Binance

pd.set_option('display.max_columns', 75)
pd.set_option('display.width', 200)
pd.set_option('display.max_rows', 150)


log = logging.getLogger('test')

@pytest.fixture()
def credential():
    return dict(api_key=None, api_secret=None)

@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_symbol_list(credential):
    binance_client = Binance(credential, log)
    await binance_client.connect()
    df = await binance_client.get_symbol_list()
    await binance_client.disconnect()
    # print(df)
    print(pd.DataFrame.from_records(df))




