import shelve
import asyncio
import datetime
import asyncio

from aiogram.utils import executor

from mics import dp, bot
import handlers

import commands


if __name__ == "__main__":
    print(f'START {datetime.datetime.now()}')
    executor.start_polling(dp, skip_updates=True, on_startup=commands.startup)
