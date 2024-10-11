
from abc import ABCMeta, abstractmethod, abstractproperty, ABC
from typing import NamedTuple
import logging
import asyncio
from typing import Callable, Coroutine, Iterable, List, Optional
from itertools import chain
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


class GetRequest(NamedTuple):
    """
    Multiple Get Request params for each of them
    """
    path: str
    params: dict | None = None


class Connector(ABC):
    _metaclass__ = ABCMeta
    code = __name__
    description = __doc__
    api_key = None
    api_secret = None
    _client = None
    log: logging.Logger
    BASE_URL: str

    def __init__(self, name: str, credential: dict | None = None, log: logging.Logger | None = None):
        self.name = name.upper()
        if log is None:
            self.log = logging.getLogger()
        else:
            self.log = log
        if credential:
            self.api_key = credential['api_key']
            self.api_secret = credential['api_secret']

    @staticmethod
    async def _aworker(
            coroutine: Coroutine,
            tasks_queue: asyncio.Queue,
            result_queue: asyncio.Queue,
            stop_event: asyncio.Event,
            timeout: float = 1,
            callback: Optional[Callable] = None
    ) -> None:
        while not stop_event.is_set() or not tasks_queue.empty():
            try:
                idx, arg = await asyncio.wait_for(tasks_queue.get(), timeout)
            except asyncio.TimeoutError:
                continue
            try:
                result = await coroutine(*arg if isinstance(arg, GetRequest) else arg)
                # result = await coroutine(arg)
                result_queue.put_nowait((idx, result))
            finally:
                tasks_queue.task_done()
                if callback is not None:
                    callback(idx, arg)

    async def _amap(
            self,
            coroutine: Coroutine,
            data: Iterable,
            max_concurrent_tasks: int = 10,
            max_queue_size: int = -1,  # infinite
            callback: Optional[Callable] = None,
    ) -> List:
        tasks_queue = asyncio.Queue(max_queue_size)
        result_queue = asyncio.PriorityQueue()

        stop_event = asyncio.Event()
        workers = [
            asyncio.create_task(self._aworker(
                coroutine, tasks_queue, result_queue, stop_event, callback=callback
            ))
            for _ in range(max_concurrent_tasks)
        ]

        for arg in enumerate(data):
            await tasks_queue.put(arg)
        stop_event.set()

        await asyncio.gather(*workers)
        await tasks_queue.join()

        results = []
        while not result_queue.empty():
            _, res = result_queue.get_nowait()
            results.append(res)
        return results

    def get_name(self):
        return self.name

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError

    async def _get(self, path: str, params: dict | None = None) -> list | dict:
        url = f'{self.BASE_URL}/{path}'
        resp = await self._client.get(url, params=params)
        return await resp.json()

    async def _get_multiple(self, requests: list[GetRequest]) -> list | dict:
        res = self._amap(self._get, requests)
        return list(chain.from_iterable(res))

    @abstractmethod
    async def get_symbol_list(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

class ConnectorSocket(Connector, ABC):
    socket = None
    client = None
    # def __init__(self, name: str):
    #     self.name = name.upper()
    #
    # def get_name(self):
    #     return self.name

