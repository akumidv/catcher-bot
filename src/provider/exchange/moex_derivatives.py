import asyncio
import os
import datetime
import aiohttp

import pandas as pd
from typing import Literal
from provider.connector import Connector
from etl.data_entities import AssetType, OptionType
from functools import wraps
import logging
from itertools import chain

IS_DEVELOP = os.environ.get('PYTHON_MODE') == 'development' or os.environ.get('PYTEST_VERSION') is not None

DEV_CACHE_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../.cache_data/MOEX'))

if IS_DEVELOP:
    os.makedirs(DEV_CACHE_PATH, exist_ok=True)

TYPE_TO_MOEX_ASSET_TYPE = {
    AssetType.FUTURE.code: 'futures',
    AssetType.SHARE.code: "share",
    AssetType.COMMODITIES.code: "commodity",
    AssetType.CURRENCY.code: 'currency',
    AssetType.INDEX.code: 'index',
}


def day_cache_async(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        def _get_key(data_type) -> tuple[int, str]:  # , *_args, **_kwargs
            key_args = list(args[1:]) + [kwargs[key] for key in kwargs] if kwargs else list(args[1:])
            params_str = (','.join([str(val) for val in key_args]) if len(key_args) != 0 else '')
            key_str = data_type if not params_str else data_type + '_' + params_str
            # get_sha256 = lambda text_str: int(hashlib.sha256(text_str.encode('utf-8')).hexdigest(), 16) % (10 ** 16)
            # key = get_sha256(key_str)
            return key_str  # key

        fn_path = None
        if IS_DEVELOP:
            fn_path = os.path.join(DEV_CACHE_PATH, f'{_get_key(func.__name__)}.parquet')
            if os.path.exists(fn_path) and \
                    datetime.date.today() != datetime.date.fromtimestamp(os.path.getmtime(fn_path)) + \
                    datetime.timedelta(days=1):
                print(f'From cache {func.__name__}:', fn_path)
                return pd.read_parquet(fn_path)
        res = await func(*args, **kwargs)
        if isinstance(res, pd.DataFrame) and fn_path is not None:
            res.to_parquet(fn_path)
        return res

    return wrapped


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
        df = self._convert_date(df)
        df['underlying_code'] = df['symbol'] + '.' + df['type'].str.upper() + '/MOEX'
        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns_rename = self._filter_dict_by_column(df.columns,
                                                     {'asset_code': 'symbol', 'asset_type': 'type',
                                                      'asset_subtype': 'subtype', 'title': 'name'})
        if columns_rename:
            df.rename(columns=columns_rename, inplace=True)
        return df

    def _convert_values(self, df: pd.DataFrame, columns: list | None = None):
        type_replace_dict = {'futures': AssetType.FUTURE.code,
                             'index': AssetType.INDEX.code,
                             'share': AssetType.SHARE.code,
                             'currency': AssetType.CURRENCY.code,
                             'commodity': AssetType.COMMODITIES.code}
        columns_retype = self._filter_list_by_column(df.columns, columns if columns else ['type', 'subtype'])
        if type_replace_dict:
            df[columns_retype] = df[columns_retype].replace(type_replace_dict)
        if 'option_type' in df.columns:
            df['option_type'] = df['option_type'].replace({OptionType.CALL.value: OptionType.CALL.code,
                                                           OptionType.PUT.value: OptionType.PUT.code})
        return df

    @staticmethod
    def _filter_list_by_column(columns: pd.Index, rename_list: list):
        return [col for col in rename_list if col in columns]

    @staticmethod
    def _filter_dict_by_column(columns: pd.Index, rename_dict: dict):
        return {col: rename_dict[col] for col in rename_dict if col in columns}

    def _convert_date(self, df: pd.DataFrame, columns: list | None = None):
        date_columns = self._filter_list_by_column(df.columns, columns if columns is not None else [
            'expiration_date'
        ])
        df[date_columns] = df[date_columns].apply(pd.to_datetime, axis='columns')
        return df

    @day_cache_async
    async def get_symbol_list(self, underlying_type: Literal[
                                                         'futures', 'currency', 'share', 'index', 'commodity'] | None = None) -> pd.DataFrame:
        """
             symbol name               type subtype  underlying_code
        0    ABIO   ABIO (iАРТГЕН ао)   s    None     ABIO.S_MOEX
        3    AFLT   AFLT (Аэрофлот)    s    None     AFLT.S_MOEX
        4    AFLT   AFLT (фьючерс)     f    s        AFLT.F_MOEX
        89   WHEAT  WHEAT (фьючерс)    f    g        WHEAT.F_MOEX
        90   YDEX   YDEX (ЯНДЕКС)      s    None     YDEX.S_MOEX
        """
        assert underlying_type is None or underlying_type in ['futures', 'currency', 'share', 'index', 'commodity']
        params = {'asset_type': underlying_type} if underlying_type else None
        underlyings = await self._get('assets', params=params)
        und_df = pd.DataFrame.from_records(underlyings)
        und_df = self._data_normalization(und_df)
        return und_df

    @day_cache_async
    async def get_futures_list(self, futures: list | None = None, expiration_dates: list | None = None) -> pd.DataFrame:
        if futures is None:
            und_df = await self.get_symbol_list(underlying_type='futures')
            futures = list(und_df[und_df['type'] == AssetType.FUTURE.code]['symbol'].unique())[:5]
            expiration_dates = [None] * len(futures)
        elif expiration_dates is None or len(futures) != len(expiration_dates):
            expiration_dates = [None] * len(futures)
        tasks = []
        for future_code, expiration_date in zip(futures, expiration_dates):
            params = {'expiration_date': expiration_date} if expiration_date is not None else None
            tasks.append(self._get(f'assets/{future_code}/futures', params))
        results = await self._gather_with_concurrency(*tasks)
        res = list(chain.from_iterable(results))
        futures_df = pd.DataFrame.from_records(res)
        futures_df = self._data_normalization(futures_df)
        return futures_df

    @day_cache_async
    async def get_options_list(self, options_symbols_df: pd.DataFrame | None = None) -> pd.DataFrame:
        if options_symbols_df is None:
            all_options_symbols_df = await self.get_symbol_list()
            options_symbols_df = all_options_symbols_df[['symbol', 'type']]
        tasks = []
        for idx, opt_row in options_symbols_df.iterrows():
            print(idx, opt_row['symbol'], opt_row['type'], TYPE_TO_MOEX_ASSET_TYPE.get(opt_row['type']))
            params = {'asset_type': TYPE_TO_MOEX_ASSET_TYPE.get(opt_row['type'])}
            if 'expiration_date' in options_symbols_df:
                params.update = {'expiration_date': opt_row['expiration_date']}
            tasks.append(self._get(f'assets/{opt_row["symbol"]}/options', params))
        results = await self._gather_with_concurrency(*tasks)
        res = list(chain.from_iterable(results))
        options_df = pd.DataFrame.from_records(res)
        options_df = self._data_normalization(options_df)
        return options_df
