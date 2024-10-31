import asyncio
import datetime

import pandas as pd
import pytest
import os
from provider.exchange.moex_derivatives import MoexOptions
from provider.data_entities import AssetType, OptionType
from tests.utiltest import check_df_columns, check_all_column_values_in_set


TYPE_CODES = [AssetType.FUTURE.code, AssetType.INDEX.code, AssetType.SHARE.code,  AssetType.CURRENCY.code,
              AssetType.COMMODITIES.code]
OPT_TYPES_CODES = [OptionType.CALL.code, OptionType.PUT.code]

@pytest.fixture
def moex_client() -> MoexOptions:
    moex_client = MoexOptions()
    # if not moex_client.is_connected:
    # await moex_client.connect()
    # return moex_client
    yield moex_client
    # asyncio.get_event_loop().run_until_complete(moex_client.disconnect())


def test__convert_dates(moex_client):
    df = pd.DataFrame([{'expiration_date': '2021-10-14'}, {'expiration_date': '2022-10-14'}])
    assert isinstance(df.iloc[0]['expiration_date'], str)
    df = moex_client._convert_date(df)
    assert isinstance(df.iloc[0]['expiration_date'], pd.Timestamp)
    assert df.dtypes['expiration_date'] == 'datetime64[ns]'


def test__convert_values(moex_client):
    df = pd.DataFrame([{'underlying_type': 'futures'}, {'underlying_type': 'index'}])
    df = moex_client._convert_values(df)
    types_list = list(df['underlying_type'].unique())
    assert AssetType.FUTURE.code in types_list
    assert AssetType.INDEX.code in types_list


@pytest.mark.asyncio
async def test_get_symbol_list(moex_client):
    und_df = await moex_client.get_symbol_list()
    assert isinstance(und_df, pd.DataFrame)
    check_df_columns(und_df.columns, ['underlying_id', 'underlying_type', 'exchange_symbol', 'name'])
    check_all_column_values_in_set(und_df['underlying_type'].unique(), TYPE_CODES)

@pytest.mark.asyncio
async def test_get_futures_list(moex_client):
    futures_df = await moex_client.get_futures_list()
    assert isinstance(futures_df, pd.DataFrame)
    check_df_columns(futures_df.columns, ['exchange_future_id', 'exchange_symbol', 'underlying_type', 'expiration_date', 'underlying_id'])
    assert isinstance(futures_df.iloc[0]['expiration_date'], pd.Timestamp)
    check_all_column_values_in_set(futures_df['underlying_type'], TYPE_CODES)

@pytest.mark.asyncio
async def test_get_options_list(moex_client):
    options_df = await moex_client.get_options_list()
    options_df.attrs = {'data_type': 'options_list', 'datetime': datetime.datetime.now().isoformat()}
    assert isinstance(options_df, pd.DataFrame)
    check_df_columns(options_df.columns, ['exchange_future_id', 'exchange_symbol', 'underlying_type', 'expiration_date', 'underlying_id',
                                          'exchange_option_id',  'series_type', 'strike', 'option_type'])
    assert isinstance(options_df.iloc[0]['expiration_date'], pd.Timestamp)
    check_all_column_values_in_set(options_df['underlying_type'], TYPE_CODES)
    # print(options_df[options_df['exchange_symbol']=='BR'])

@pytest.mark.asyncio
async def test_get_option_series(moex_client):
    options_df = await moex_client.get_option_series()
    # options_df.attrs = {'data_type': 'options_list', 'datetime': datetime.datetime.now().isoformat()}
    assert isinstance(options_df, pd.DataFrame)
    # check_df_columns(options_df.columns, ['exchange_future_id', 'exchange_symbol', 'type', 'expiration_date', 'underlying_id',
    #                                       'exchange_option_id',  'series_type', 'strike', 'option_type'])
    assert isinstance(options_df.iloc[0]['expiration_date'], pd.Timestamp)
    check_all_column_values_in_set(options_df['underlying_type'], TYPE_CODES)
    # print(options_df)
    # print(options_df[options_df['exchange_symbol']=='BR'])


@pytest.mark.asyncio
async def test_get_option_for_id(moex_client):
    options_list_df = await moex_client.get_options_list()
    options_list_df = options_list_df[options_list_df['exchange_symbol']=='BR']
    options_df = await moex_client.get_option_for_id(options_list_df)
    assert isinstance(options_df, pd.DataFrame)
    print(options_df)
    check_df_columns(options_df.columns, ['delta', 'gamma', 'vega', 'theta', 'rho', 'exchange_option_id', 'days_until_expiring',
                                          'underlying_price', 'volatility', 'underlying_id',  'theorprice', # 'underlying_type',
                                          'fee', 'expiring_date', 'lastprice', 'settleprice'])
    # assert isinstance(options_df.iloc[0]['expiration_date'], pd.Timestamp)
    check_all_column_values_in_set(options_df['option_type'].unique(), OPT_TYPES_CODES)
    # print(options_df[options_df['exchange_symbol']=='BR'])


@pytest.mark.asyncio
async def test_get_options(moex_client):
    options_df = await moex_client.get_options()
    assert isinstance(options_df, pd.DataFrame)
    check_df_columns(options_df.columns, ['delta', 'gamma', 'vega', 'theta', 'rho', 'exchange_option_id', 'theorprice',
                                          'theorprice_rub', 'last', 'offer', 'bid', 'numtrades', 'strike', 'volatility',
                                          'intrinsic_value', 'timed_value', 'exchange_future_id', 'expiration_date',
                                          'option_type', 'underlying_id', 'currency', 'underlying_price',
                                          'fee', 'lastprice', 'settleprice'])
    assert isinstance(options_df.iloc[0]['expiration_date'], pd.Timestamp)
    check_all_column_values_in_set(options_df['option_type'].unique(), OPT_TYPES_CODES)

import pandas_market_calendars as mcal
import exchange_calendars as xcals
def test_a():
    moex_cal = mcal.get_calendar('NYSE') #MOEX
    print(moex_cal.tz.zone)
    # print(moex_cal.holidays().holidays)
    print(moex_cal.regular_market_times)
    # ext = moex_cal.schedule(start_date = pd.Timestamp().now(), end_date=pd.Timestamp().now(), start="pre", end="post")
    # print(ext)
    # print(moex_cal.open_at_time(ext, pd.Timestamp('2012-07-03 12:00', tz='America/New_York')))
    # print(moex_cal.open_at_time(ext, pd.Timestamp().now()))

    print(xcals.get_calendar_names(include_aliases=False))
    xmoex = xcals.get_calendar("XMOS")
    print(xmoex.schedule.loc["2024-10-01":"2024-10-30"])

@pytest.mark.asyncio
async def test_get_working_calendar(moex_client):
    calendar = await moex_client.get_calendar()
