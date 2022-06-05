import asyncio
from datetime import datetime
from email import message
from re import I
import sys

from utils import get_double_messages, parse_entities

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
from PyrogramToAiogramConvertor import convert
from aiogram.utils.text_decorations import HtmlDecoration
from loguru import logger


@app.on_message(filters.forwarded & filters.text & filters.channel)
async def echo(client, message_app):
    # if not check_message_in_base(message_app):
    #     return 0
    stop_user_ids = get_double_messages(message_app.text)
    logger.info(f"[{datetime.now()}] Stop_user_id: {stop_user_ids}")
    session = Session()
    try:
        channel_link = (
            session.query(Channel)
            .filter_by(сhannel_id=message_app.chat.id)
            .first()
            .get_link()
        )
    except Exception as er:
        logger.error(f"[{datetime.now()}] Error: {er}")
        return 0
    try:
        all_user = [
            i.user_id
            for i in (
                session.query(Channel)
                .filter_by(сhannel_id=message_app.chat.id)
                .first()
                .subs
            )
        ]

    except Exception as er:
        logger.error(f"[{datetime.now()}] Error: {er}")
        all_user = []
    session.close()

    actual_all_user = []
    for i in all_user:
        if not (i in stop_user_ids):
            actual_all_user.append(i)
    logger.info(
        f"[{datetime.now()}] Send message in text with forward. Users: [{actual_all_user}]\n Message entity:\n {str(message_app)}"
    )
    for user in actual_all_user:
        try:
            await bot.send_message(
                user,
                f"""<a href="{channel_link}">{message_app.chat.title}</a>
Forwarded from <a href="https://t.me/{message_app.forward_from_chat.username}">{message_app.forward_from_chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
            )
        except Exception as er:
            logger.error(f"[{datetime.now()}] Error: {er}")
    session = Session()
    for user in actual_all_user:
        new_message = Message(
            chat_id=message_app.chat.id,
            message_id=message_app.id,
            text=message_app.text,
            user_id=user,
        )
        session.add(new_message)
        session.commit()
    session.close()
