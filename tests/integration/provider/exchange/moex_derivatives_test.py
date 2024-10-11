import asyncio

import pandas as pd
import pytest

from provider.exchange.moex_derivatives import MoexOptions
from etl.data_entities import AssetType

moex_client = MoexOptions()

async def get_client() -> MoexOptions:
    if not moex_client.is_connected:
        await moex_client.connect()
    return moex_client
    # yield moex_client
    # asyncio.get_event_loop().run_until_complete(moex_client.disconnect())


@pytest.mark.asyncio
async def test_get_symbol_list():
    client = await get_client()
    und_df = await client.get_symbol_list()
    print(und_df)
    assert isinstance(und_df, pd.DataFrame)
    assert 'underlying_code' in und_df.columns
    assert 'type' in und_df.columns
    assert 'symbol' in und_df.columns


    # async with MoexOptions() as moex_client:
    #     if not moex_client.is_connected:
    #         await moex_client.connect()
    #         print("#######", moex_client.is_connected)
    # print(client.is_connected())
    # print('###!!!!', )
    # await client.get_symbol_list()
