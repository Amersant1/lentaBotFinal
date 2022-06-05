from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


from databases import Base
from pyrogram import Client, filters


import os
from config import token, api_id, api_hash

bot = Bot(token,parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())

app = Client("my_account", api_id, api_hash)
bot_app = Client(
    "my_bot",
    bot_token=token
)
service_bot = "@test_LR_bot"



engine = create_engine(f"sqlite:///base")

Base.metadata.create_all(engine)

if not os.path.isfile(f"./base"):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
