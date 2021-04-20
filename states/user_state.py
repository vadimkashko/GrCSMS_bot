from aiogram.dispatcher.filters.state import StatesGroup, State


# Группа состояний пользователя
class UserState(StatesGroup):
    start_menu = State()                # Нахождение в стартовом меню бота
    input_unp = State()                 # Готов к вводу УНП или кода заказчика
    input_order_number = State()        # Готов к вводу номера заказа
    get_company_info = State()          # Получены реквизиты
    get_location = State()              # Получено местоположение
    get_contacts = State()              # Получены контакты
