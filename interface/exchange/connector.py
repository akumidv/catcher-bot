import datetime
import math
import asyncio
import importlib

WEIGHT_PER_REQUEST = 1
WEIGHT_LIMIT = 2200
API_WEIGHT = {
    'default': WEIGHT_PER_REQUEST,
}
USED_WEIGHT = {'request_time': datetime.datetime.fromtimestamp(0), 'used_weight': 0, 'is_showed': False}


async def _wait_for_next_request(): # TODO add exhcnage type and there are limits and weight (init form exchange module)
    global USED_WEIGHT
    cur_datetime = datetime.datetime.now()
    cur_minute = cur_datetime.replace(second=0, microsecond=0)
    if USED_WEIGHT['request_time'] == cur_minute:
        USED_WEIGHT['weight'] += WEIGHT_PER_REQUEST #API_WEIGHT.get(method, WEIGHT_PER_REQUEST)
        if USED_WEIGHT['weight'] > WEIGHT_LIMIT:
            time_difference = (cur_minute + datetime.timedelta(minutes=1)) - cur_datetime
            seconds_for_wait = math.ceil(time_difference.total_seconds())
            if not USED_WEIGHT['is_showed']:
                USED_WEIGHT['is_showed'] = True
                print(f"[WARNING] Wait for next request {seconds_for_wait} used weight {USED_WEIGHT['weight']}"
                      f" for {USED_WEIGHT['request_time']}")
            await asyncio.sleep(seconds_for_wait)
    else:
        USED_WEIGHT['request_time'] = cur_minute
        USED_WEIGHT['weight'] = WEIGHT_PER_REQUEST
        USED_WEIGHT['is_showed'] = False


def init_exchange(exchange_name, credential, is_socket: bool = False, market_type: str = 'stock'):
    exchange_module = importlib.import_module(f'interface.exchange.{exchange_name}_class', exchange_name) #'subscriber')#'interface/exchange', name)
    class_name = exchange_name[0].upper() + exchange_name[1:].lower()
    if is_socket:
        class_name += 'Socket'
    if market_type == 'futures':
        class_name += 'Futures'
    exchange = exchange_module.__getattribute__(class_name)(credential)
    return exchange


