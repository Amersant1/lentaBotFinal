import asyncio
from datetime import datetime
from email import message
import imp
from re import I
import sys

from utils import check_сhannels

sys.path.append("../")
from pyrogram import Client, filters
from pyrogram.parser import Parser
from mics import dp, bot, app, Session
from databases import Message, User, Channel, Subscribe
from aiogram.types import ParseMode
from apscheduler.schedulers.background import BackgroundScheduler
from aiogram.types.input_media import (
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    InputFile,
    MediaGroup,
)
from aiogram.types.message_entity import MessageEntity, MessageEntityType
from config import bot_name
from html_parser import unparse
import logging
from PyrogramToAiogramConvertor import convert
from aiogram.utils.text_decorations import HtmlDecoration
from loguru import logger

logger.add("file_{time}.log")
import forward_text_hand
import forward_media_group_hand
import forward_media_hand
import text_hand
import media_group_hand
import media_hand


# logging.basicConfig(filename="sample.log", level=logger.INFO)

# service_bot = bot_name


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_сhannels, "interval", seconds=10)
    scheduler.start()
    print("Client started")
    app.run()
