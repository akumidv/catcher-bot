
from enum import Enum


class AssetType(str, Enum):
    OPTION_CALL = "call", "c"
    OPTION_PUT = "put", "p"
    FUTURE = "future", 'f'
    SHARE = "share", 's'
    STOCK = "stock", 's'
    CRYPTO = "cryptocurrency", 'x'
    COMMODITIES = "commodities", 'g' # goods
    CURRENCY = 'currency', 'm' # money
    INDEX = 'index', 'i'

    def __new__(cls, value, code):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.code = code
        return obj

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


ASSET_TYPE_MAP = {
    AssetType.OPTION_CALL.code: AssetType.OPTION_CALL,
    AssetType.OPTION_PUT.code: AssetType.OPTION_PUT,
    AssetType.FUTURE.code: AssetType.FUTURE,
    AssetType.SHARE.code: AssetType.SHARE,
    AssetType.CRYPTO.code: AssetType.CRYPTO,
    AssetType.COMMODITIES.code: AssetType.COMMODITIES,
    AssetType.INDEX.code: AssetType.INDEX,
}
