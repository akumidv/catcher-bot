import importlib
import logging

def init_exchange(exchange_name, credential, is_socket: bool = False, market_type: str = 'stock'):
    exchange_module = importlib.import_module(f'interface.exchange.{exchange_name}_class', exchange_name) #'subscriber')#'interface/exchange', name)
    class_name = exchange_name[0].upper() + exchange_name[1:].lower()
    if is_socket:
        class_name += 'Socket'
    if market_type == 'futures':
        class_name += 'Futures'
    exchange = exchange_module.__getattribute__(class_name)(credential, logging.getLogger(exchange_name))
    # TODO
    return exchange
