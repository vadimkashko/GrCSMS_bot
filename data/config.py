from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")            # Забираем значение типа str
ADMINS = env.list("ADMINS")                 # Тут у нас будет список из админов
IP = env.str("IP")                          # Тоже str, но для айпи адреса хоста
BOT_COMMANDS = env.dict("BOT_COMMANDS")     # Словарь из команд для бота
ORDERS_XML = env.str("ORDERS_XML")          # Ссылка на xml-файл с заказами
