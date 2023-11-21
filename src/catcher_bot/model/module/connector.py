
from abc import ABCMeta, abstractmethod, abstractproperty, ABC
#from core.bot_context import BotContext
import logging

# import datetime
# import math
# import asyncio
# WEIGHT_PER_REQUEST = 1
# WEIGHT_LIMIT = 2200
# API_WEIGHT = {
#     'default': WEIGHT_PER_REQUEST,
# }
# USED_WEIGHT = {'request_time': datetime.datetime.fromtimestamp(0), 'used_weight': 0, 'is_showed': False}
#
# async def _wait_for_next_request():  # TODO add exhcnage type and there are limits and weight (init form exchange module)
#     global USED_WEIGHT
#     cur_datetime = datetime.datetime.now()
#     cur_minute = cur_datetime.replace(second=0, microsecond=0)
#     if USED_WEIGHT['request_time'] == cur_minute:
#         USED_WEIGHT['weight'] += WEIGHT_PER_REQUEST #API_WEIGHT.get(method, WEIGHT_PER_REQUEST)
#         if USED_WEIGHT['weight'] > WEIGHT_LIMIT:
#             time_difference = (cur_minute + datetime.timedelta(minutes=1)) - cur_datetime
#             seconds_for_wait = math.ceil(time_difference.total_seconds())
#             if not USED_WEIGHT['is_showed']:
#                 USED_WEIGHT['is_showed'] = True
#                 print(f"[WARNING] Wait for next request {seconds_for_wait} used weight {USED_WEIGHT['weight']}"
#                       f" for {USED_WEIGHT['request_time']}")
#             await asyncio.sleep(seconds_for_wait)
#     else:
#         USED_WEIGHT['request_time'] = cur_minute
#         USED_WEIGHT['weight'] = WEIGHT_PER_REQUEST
#         USED_WEIGHT['is_showed'] = False


class Connector(ABC):
    _metaclass__ = ABCMeta
    code = __name__
    description = __doc__

    client = None

    def __init__(self, name: str, credential: dict, log: logging.Logger):
        self.name = name.upper()
        self.log = log
        self.api_key = credential['api_key']
        self.api_secret = credential['api_secret']

    def get_name(self):
        return self.name

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError


    @abstractmethod
    async def get_symbol_list(self):
        raise NotImplementedError


class ConnectorSocket(Connector, ABC):
    socket = None
    client = None
    # def __init__(self, name: str):
    #     self.name = name.upper()
    #
    # def get_name(self):
    #     return self.name

