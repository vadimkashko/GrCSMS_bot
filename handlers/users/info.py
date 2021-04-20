import logging
import emoji

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import return_keyboard
from loader import dp
from states import UserState


# Ловит нажатие на инлайн-кнопку "Реквизиты" и сообщает пользователю реквизиты
@dp.callback_query_handler(text_contains="about company", state=UserState.start_menu)
async def send_info_about_company(call: CallbackQuery, state: FSMContext):
    logging.info(call.data)
    await call.message.delete_reply_markup()
    await call.answer(cache_time=60)
    await call.message.answer(text=emoji.emojize(string="Республиканское унитарное предприятие «Гродненский центр "
                                                 "стандартизации, метрологии и сертификации»\nГродненский ЦСМС\n\n"
                                                 f":office:: пр-т Космонавтов, 56, г. Гродно, Республика Беларусь, "
                                                 f"230003.\n\nУНП 500028553 ОКПО 02568443\nДирекция ОАО "
                                                 f"\"БЕЛИНВЕСТБАНК\" по Гродненской области, BIC BLBBBY2X, "
                                                 f"р/с BY81BLBB30120500028553001001\n\n"
                                                 f":telephone:: +375 (152) 64 31 41\n:fax:: +375 (152) 64 31 29"
                                                 f"\n:e-mail:: csms@csms.grodno.by", use_aliases=True),
                              reply_markup=return_keyboard)
    await state.set_state(UserState.get_company_info)


# Ловит нажатие на инлайн-кнопку "Как проехать" и сообщает пользователю реквизиты
@dp.callback_query_handler(text_contains="location", state=UserState.start_menu)
async def send_location(call: CallbackQuery, state: FSMContext):
    logging.info(call.data)
    await call.message.delete_reply_markup()
    await call.answer(cache_time=60)
    await call.message.answer_location(latitude=53.670659, longitude=23.850198)
    await call.message.answer(text=emoji.emojize(string="Вы можете перейти к навигации :round_pushpin:, нажав на "
                                                        "изображение выше этого сообщения.", use_aliases=True),
                              reply_markup=return_keyboard)
    await state.set_state(UserState.get_location)


# Ловит нажатие на инлайн-кнопку "Контакты" и сообщает пользователю номера телефонов
@dp.callback_query_handler(text_contains="contacts", state=UserState.start_menu)
async def send_contacts(call: CallbackQuery, state: FSMContext):
    logging.info(call.data)
    await call.message.delete_reply_markup()
    await call.answer(cache_time=60)
    await call.message.answer(text=emoji.emojize(string=f"Бюро приемки:\n:telephone:: +375 (152) 71 45 91\n"
                                                        f":telephone:: +375 (152) 71 45 92\n:fax:: +375 (152) 71 45 93\n"
                                                        f":e-mail:: gruppa_pp@csms.grodno.by\n\n"
                                                        f"Сектор электроизмерений и радиоизмерений:\n"
                                                        f":telephone:: +375 (152) 71 45 88\n"
                                                        f":telephone:: +375 (152) 71 45 89\n"
                                                        f":iphone:: +375 (29) 822 18 52\n"
                                                        f":e-mail:: sector_eri@csms.grodno.by\n\n"
                                                        f"Сектор измерений механических и геометрических величин:\n"
                                                        f":telephone:: +375 (152) 71 45 97\n"
                                                        f":e-mail:: sector_imgv@csms.grodno.by\n\n"
                                                        f"Сектор теплотехнических и физико-химических измерений:\n"
                                                        f":telephone:: +375 (152) 71 45 94\n"
                                                        f":e-mail:: sector_tfhi@csms.grodno.by\n\n",
                                                 use_aliases=True),
                              reply_markup=return_keyboard)
    await state.set_state(UserState.get_company_info)
