from aiogram import types

from mics import bot


async def startup(message):
    bot_commands = [
        types.BotCommand(command="/help", description="Помощь"),
        types.BotCommand(command="/find", description="Найти похожые каналы"),
        types.BotCommand(command="/report", description="Репорт"),
        types.BotCommand(command="/list", description="Список подписок"),
    ]
    await bot.set_my_commands(bot_commands)
