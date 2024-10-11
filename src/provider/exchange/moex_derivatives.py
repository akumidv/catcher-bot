import asyncio
import aiohttp
import asyncio

import pandas as pd

from provider.connector import Connector, GetRequest
from etl.data_entities import AssetType
import logging


class MoexOptions(Connector):
    """
    API Swagger Doc https://iss.moex.com/iss/apps/option-calc/v1/docs

    """
    _client: aiohttp.ClientSession | None = None
    log: logging.Logger
    BASE_URL = 'https://iss.moex.com/iss/apps/option-calc/v1'

    async def __aenter__(self):
        self._client = aiohttp.ClientSession()
        print('CONNECTED')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.is_connected:
            await self._client.close()
            self._client = None

    def __init__(self, credential: dict | None = None, log: logging.Logger = None):
        super().__init__('MOEX Derivatives', credential, log)

    @property
    def is_connected(self):
        return self._client is not None

    async def connect(self):
        if not self.is_connected:
            self._client = aiohttp.ClientSession()
        else:
            logging.warning('MOEX already connected')
        return self._client


    async def disconnect(self):
        if self._client is not None:
            await self._client.close()
            self._client = None
        else:
            logging.warning('MOEX already closed')

    def _data_normalization(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._rename_columns(df)
        df = self._convert_values(df)
        df['underlying_code'] = df['symbol'] + '.' + df['type'].str.upper() + '_MOEX'
        return df

    @staticmethod
    def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns={'asset_code': 'symbol', 'asset_type': 'type',
                           'asset_subtype': 'subtype', 'title': 'name'}, inplace=True)
        return df

    @staticmethod
    def _convert_values(df: pd.DataFrame):
        replace_dict = {'futures': AssetType.FUTURE.code, 'index': AssetType.INDEX.code,
                        'share': AssetType.SHARE.code, 'currency': AssetType.CURRENCY.code,
                        'commodity': AssetType.COMMODITIES.code}
        df['type'] = df['type'].replace(replace_dict)
        df['subtype'] = df['subtype'].replace(replace_dict)
        return df

    async def get_symbol_list(self, underlying_type: str | None = None) -> pd.DataFrame:
        assert underlying_type is None or underlying_type in ['future', 'currency', 'share']
        params = {'asset_type': underlying_type} if underlying_type else None
        underlyings = await self._get('assets', params=params)
        und_df = pd.DataFrame.from_records(underlyings)
        und_df = self._data_normalization(und_df)
        return und_df

    async def get_futures_list(self, futures: list | None = None):
        if futures is None:
            und_df = self.get_symbol_list(underlying_type='future')
            futures = und_df[und_df['type'] == AssetType.FUTURE.code]['type'].unique()

        assets = await self._get('assets', {})