import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import BOT_COMMANDS
from loader import dp


# Ловит команду /help и выводит доступные пользователю команды
# Баг: долгая обработка первого после запуска бота использования команды /help
@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    logging.info("help")
    commands = []
    for command, description in BOT_COMMANDS.items():
        commands.append(f"/{command} - {description}")
    commands = '\n'.join(commands)
    # await message.delete()
    await message.answer(text=f"{commands}")
