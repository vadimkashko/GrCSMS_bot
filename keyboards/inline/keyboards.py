import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Стартовая inline-клавиатура с тремя кнопками
start_keyboard = InlineKeyboardMarkup()

check_order_button = InlineKeyboardButton(text=emoji.emojize(string="Проверить статус заказа :check_box_with_check:",
                                                             use_aliases=True),
                                          callback_data="check order")
start_keyboard.add(check_order_button)

about_company_button = InlineKeyboardButton(text=emoji.emojize(string="Реквизиты :bank:",
                                                               use_aliases=True),
                                            callback_data="about company")
start_keyboard.add(about_company_button)

location_button = InlineKeyboardButton(text=emoji.emojize(string="Как проехать :round_pushpin:",
                                                          use_aliases=True),
                                       callback_data="location")
start_keyboard.add(location_button)

contacts_button = InlineKeyboardButton(text=emoji.emojize(string="Контакты :notebook:",
                                                          use_aliases=True),
                                       callback_data="contacts")
start_keyboard.add(contacts_button)


# Клавиатура с одной кнопкой возврата в предыдущее меню
return_keyboard = InlineKeyboardMarkup()

return_button = InlineKeyboardButton(text=emoji.emojize(string="В начало :arrow_upper_left:", use_aliases=True),
                                     callback_data="to start")
return_keyboard.add(return_button)