import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from keyboards import start_keyboard
from loader import dp
from states import UserState


# Ловит команду /start, привествует пользователя, выводит стартовое меню
# и переводит пользователя в состояние просмотра стартового меню
@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    logging.info("start")
    # await message.delete()
    await message.answer(text=f"Здравствуйте, <b>{message.from_user.full_name}</b>!\n\nВас приветствует бот отдела "
                              f"метрологии Гродненского ЦСМС. Я помогу Вам отследить статус Вашего заказа или получить "
                              f"другую информацию.\n\nВыберите дальнейшее действие, нажав кнопку под этим сообщением.",
                         reply_markup=start_keyboard)
    await state.reset_state()
    await state.set_state(UserState.start_menu)


# Ловит нажатие на инлайн-кнопку "В начало" и возвращает пользователя
# в стартовое меню со сбросом состояния
@dp.callback_query_handler(text_contains="to start", state="*")
async def return_to_start(call: CallbackQuery, state: FSMContext):
    logging.info("to start")
    await call.message.delete_reply_markup()
    await call.answer(text="Возврат в стартовое меню...", cache_time=60)
    await call.message.answer(text=f"<b>{call.from_user.full_name}</b>, Вы вернулись в главное меню бота.\n\n"
                                   f"Выберите дальнейшее действие, нажав кнопку под этим сообщением.",
                              parse_mode=types.ParseMode.HTML, reply_markup=start_keyboard)
    await state.reset_state()
    await state.set_state(UserState.start_menu)
