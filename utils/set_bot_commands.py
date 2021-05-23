import logging

from aiogram import types
from data.config import BOT_COMMANDS


# Установка комманд по умолчанию
async def set_default_commands(dp):
    setting_result = await dp.bot.set_my_commands(
        [types.BotCommand(key, value) for key, value in BOT_COMMANDS.items()]
    )
    logging.info(f"{setting_result}")
