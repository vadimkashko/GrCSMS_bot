import logging

import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline import return_keyboard
from loader import dp
from states import UserState
from utils.parse_orders import find_order


# Ловит нажатие на inline-кнопку "Проверить статус заказа" и
# меняет состояние пользователя на готовность к вводу УНП или кода Заказчика
@dp.callback_query_handler(text_contains="check order", state=UserState.start_menu)
async def check_order(call: CallbackQuery, state: FSMContext):
    logging.info(call.data)
    await call.answer(cache_time=60)
    await call.message.delete_reply_markup()
    await call.message.answer(text=f"Для проверки статуса заказа введите:\n\nдля юридического лица - <b>УНП или код "
                                   f"Заказчика</b>;\nдля физического лица - <b>код Заказчика</b>.\n\n(Код Заказчика "
                                   f"указан в квитанции-счете, полученном при оформлении заказа.)",
                              reply_markup=return_keyboard)
    await state.set_state(UserState.input_unp)


# Ловит введенный УНП или код Заказчика, проверяет на корректность
# и меняет состояние пользователя на готовность к вводу номера квитанции-счета
@dp.message_handler(state=UserState.input_unp)
async def get_unp(message: Message, state: FSMContext):
    msg_text = message.text
    logging.info(msg_text)
    if not msg_text.isdecimal():
        # await message.delete()
        await message.answer(text=f"Неверный формат введенных данных, введите еще раз.",
                             reply_markup=return_keyboard, reply=True)
    elif len(msg_text) > 9:
        # await message.delete()
        await message.answer(text=f"Скорее всего вы ввели слишком много символов, попробуйте еще раз.",
                             reply_markup=return_keyboard, reply=True)
    else:
        async with state.proxy() as data:
            if len(msg_text) < 9:
                data["customer_id"] = msg_text
            elif len(msg_text) == 9:
                data["customer_unp"] = msg_text
        # await message.delete()
        await message.answer(text=f"Теперь введите номер квитанции-счета, полученного при оформлении "
                                  f"заказа, в одном из доступных форматов:\n\n<b>- 0000000-00\n- 0000000\n- "
                                  f"0...0</b>",
                             reply_markup=return_keyboard)
        await state.set_state(UserState.input_order_number)


# Ловит введенный номер квитанции-счета, проверяет на корректность, сообщает о
# статусе заказа и возвращает состояние пользователя к начальному
@dp.message_handler(state=UserState.input_order_number)
async def get_order_number(message: Message, state: FSMContext):
    msg_text = message.text[:7]
    logging.info(msg_text)
    if not msg_text.isdecimal():
        await message.answer(text=f"Неверный формат введенных данных, введите еще раз.",
                             reply_markup=return_keyboard, reply=True)
    else:
        if len(msg_text) < 7:
            msg_text = msg_text.rjust(7, "0")
        async with state.proxy() as data:
            data["account_id"] = msg_text
        order = await find_order(data.as_dict())
        if not order:
            await message.answer(text=emoji.emojize(string=f"Заказ с номером <b>{data['account_id']}</b> не найден. "
                                                           f"Проверьте правильность введенной Вами информации.\n\nВы "
                                                           f"можете вернуться в начало или продолжить "
                                                           f"проверку, введя <b>номер следующего заказа</b>.",
                                                    use_aliases=True),
                                 reply_markup=return_keyboard)
        elif order["account_implementation_date"] == " ":
            await message.answer(text=emoji.emojize(string=f"Уважаемый представитель <b>{order['customer_name']}</b> ("
                                                           f"УНП: <b>{order['customer_unp']}</b>, код Заказчика: "
                                                           f"<b>{order['customer_id']}</b>), к сожалению Ваш заказ № "
                                                           f"<b>{order['account_displayed_id']}</b> от "
                                                           f"<b>{order['account_beginning_date']}</b> на сумму "
                                                           f"<b>{order['summ_with_nds']}</b> BYN, в том числе НДС - "
                                                           f"<b>{order['summ_nds']}</b> BYN не готов.\n\nВы можете "
                                                           f"вернуться в начало или продолжить "
                                                           f"проверку, введя <b>номер следующего заказа</b>.",
                                                    use_aliases=True),
                                 reply_markup=return_keyboard)
        else:
            await message.answer(text=f"Уважаемый представитель <b>{order['customer_name']}</b> (УНП: "
                                      f"<b>{order['customer_unp']}</b>, код Заказчика: <b>{order['customer_id']}</b>), "
                                      f"Ваш заказ № <b>{order['account_displayed_id']}</b> от "
                                      f"<b>{order['account_beginning_date']}</b> был выполнен "
                                      f"<b>{order['account_implementation_date']}</b>.\nСумма - "
                                      f"<b>{order['summ_with_nds']}</b> "
                                      f"BYN, в том числе НДС - <b>{order['summ_nds']}</b> BYN.\n\n"
                                      f"Вы можете вернуться в начало"
                                      f" или продолжить проверку, введя <b>номер следующего заказа</b>.",
                                 reply_markup=return_keyboard)
        await state.set_state(UserState.input_order_number)
