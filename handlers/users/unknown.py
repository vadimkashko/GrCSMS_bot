import logging

import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(regexp="жыве беларусь", state="*")
async def white_red_white(message: types.Message):
    await message.reply(text=emoji.emojize(string=f"Жыве вечна!!! :white_large_square::red_square::white_large_square:",
                                           use_aliases=True))


# Хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def unknown_message(message: types.Message):
    logging.info(message.text)
    await message.reply(text=emoji.emojize(string=f"Извините, в будущем я обязательно научусь с этим работать "
                                                  f":thinking_face:",
                                           use_aliases=True))


# Хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def all_unknown_messages(message: types.Message, state: FSMContext):
    state = await state.get_state()
    logging.info(message.text, state)
    await message.reply(text=emoji.emojize(string=f"Извините, в будущем я обязательно научусь с этим работать "
                                                  f":thinking_face:",
                                           use_aliases=True))
