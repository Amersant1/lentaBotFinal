from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    AwaitLink = State()
    AwaitReport = State()
    AwaitFindSingle = State()
