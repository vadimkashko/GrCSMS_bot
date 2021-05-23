import asyncio
# import logging
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


# Antiflood-middleware
class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()        # Конструктор родительского класса.

    # Непосредственно метод для троттлинга либо message, либо callback_query
    async def throttle(self, target: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()                     # Получение текущего хэндлера из контекста.
        dispatcher = Dispatcher.get_current()               # Получение диспатчера из контекста.
        if not handler:
            return

        # Получение аттрибутов функции хэндлера, установленных декоратором rate_limit,
        # или установка по умолчанию в случае их отсутствия.
        limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
        key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")

        # Троттлинг при превышении limit.
        try:
            await dispatcher.throttle(key, rate=limit)      # В случае возврата True троттлинг не включается.
        except Throttled as t:
            await self.target_throttled(target, t, dispatcher, key)
            raise CancelHandler()

    # Обработка инициатора троттлинга (message или callback_query)
    # с предупреждением пользователя о временной приостановке
    # обработки сообщений.
    @staticmethod
    async def target_throttled(target: Union[types.Message, types.CallbackQuery],
                               throttled: Throttled, dispatcher: Dispatcher, key: str):

        # Определение типа апдейта-инициатора троттлинга.
        if isinstance(target, types.CallbackQuery):
            msg = target.message
        else:
            msg = target
        delta = throttled.rate - throttled.delta            # Считает время, оставшееся до истечения лимита.
        if throttled.exceeded_count == 1:
            await msg.answer(f'Давайте попробуем не так быстро.')
            return
        elif throttled.exceeded_count == 2:
            await msg.answer(f'Вы очень настойчивы! Подожду, пока не пройдет {round(delta, 2)} с.')
            return
        await asyncio.sleep(delta)                          # Игнорирует пользователя в течение delta.

        # Возврат в нормальное состояние
        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await msg.reply("Я снова готов Вас выслушать.")

    # Точка входа для работы antiflood-middleware
    async def on_process_message(self, message, data):
        await self.throttle(message)

    # Точка входа для работы antiflood-middleware
    async def on_process_callback_query(self, call, data):
        await self.throttle(call)
