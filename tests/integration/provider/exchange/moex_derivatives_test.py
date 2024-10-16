import asyncio

import pandas as pd
import pytest
import os
from provider.exchange.moex_derivatives import MoexOptions
from etl.data_entities import AssetType
from tests.utiltest import check_df_columns, check_all_column_values_in_set
moex_client = MoexOptions()

TYPE_CODES = [AssetType.FUTURE.code, AssetType.INDEX.code, AssetType.SHARE.code,  AssetType.CURRENCY.code,
              AssetType.COMMODITIES.code]


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
    assert isinstance(und_df, pd.DataFrame)
    check_df_columns(und_df.columns, ['underlying_code', 'type', 'symbol'])
    check_all_column_values_in_set(und_df['type'].unique(), TYPE_CODES)

@pytest.mark.asyncio
async def test_get_futures_list():
    client = await get_client()
    futures_df = await client.get_futures_list()
    assert isinstance(futures_df, pd.DataFrame)
    check_df_columns(futures_df.columns, ['futures_code', 'symbol', 'type', 'expiration_date', 'underlying_code'])
    assert isinstance(futures_df.iloc[0]['expiration_date'], pd.Timestamp)
    check_all_column_values_in_set(futures_df['type'], TYPE_CODES)


def test__convert_dates():
    df = pd.DataFrame([{'expiration_date': '2021-10-14'}, {'expiration_date': '2022-10-14'}])
    assert isinstance(df.iloc[0]['expiration_date'], str)
    df = moex_client._convert_date(df)
    assert isinstance(df.iloc[0]['expiration_date'], pd.Timestamp)
    assert df.dtypes['expiration_date'] == 'datetime64[ns]'


def test__convert_values():
    df = pd.DataFrame([{'type': 'futures'}, {'type': 'index'}])
    df = moex_client._convert_values(df)
    types_list = list(df['type'].unique())
    assert AssetType.FUTURE.code in types_list
    assert AssetType.INDEX.code in types_list
