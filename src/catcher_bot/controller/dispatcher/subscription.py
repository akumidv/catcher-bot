import multiprocessing
"""TODO
- инициализируем модель подписки на цены биржи/бирж или нескльких подписок (для дробления большого кол-ва инструментов на несколько субпроцессов)
- сама подписка реализуется в модели подписок(?)
- полученные данные передаются диспетчеру
- диспетчер отправляет данные стратегиям
"""

#price = multiprocessing.Queue()
from catcher_bot.controller.strategy_dispatcher import StrategyDispatcher


class SubscriptionOrganizer:

    def __init__(self, sd: StrategyDispatcher):
        self.sd = sd


def worker_pipe_send(conn, msg, iterat):
    for i in range(iterat):
        conn.send(msg)
    conn.send('close')


def worker_pipe_receive(conn):
    while True:
        val = conn.recv()
        if val == 'close':
            break

def pipe_iter(msg, iterat, is_duplex = True):
    parent_conn, child_conn = multiprocessing.Pipe(duplex = is_duplex)
    p_send = multiprocessing.Process(target=worker_pipe_send, args=(child_conn, msg, iterat))
    p_recive = multiprocessing.Process(target=worker_pipe_receive, args=(parent_conn,))
    p_send.start()
    p_recive.start()
    p_send.join()
    p_recive.join()
