""" TODO

1. Пройтись и найти все стратегии,
2. Инициализировать стратегии, выяснить для них состав бирж и тикеров.
3. Подписать стратегию на:
    - цены с биржи
    - обновления позиций в бирже
    - обновления поданных ордеров
    - пинг проверки состояния

- при получении данных от подписки, диспетчер отправляет данные стратегиям которые подписаны на этот тикер
- стратегией может быть логгер в БД - т.е. сохраняющий все данные. Для подписки может использоваться знак * или все или какой-то ругой способ выбора всех символав и или черный/белые списки.
- эмулятор стратегии вместо биржи
"""

import os
import multiprocessing
from catcher_bot.core.bot_context import BotContext


class StrategyDispatcher:

    def __init__(self, bc: BotContext):
        self.bc = bc
        # TODO get exchanges list
        # TODO get ticker list for exchanges
        # get strategies list that contain exchanges and tickers



    def run(bc: BotContext):
        # or prepare exchanges list and tickers there?
        # init subscriptions there?

        strategy = lambda x: x # TODO mock
        jobs = []
        for i in range(4):
            p = multiprocessing.Process(target=strategy)
            jobs.append(p)
            p.start()


