import asyncio
from datetime import datetime
from email import message
from re import I
import sys

from utils import check_for_media_group, get_double_messages, parse_entities

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


@app.on_message(filters.forwarded & filters.media_group & filters.channel)
async def echo_frw(client, message_app):

    ls_of_messages = await client.get_media_group(message_app.chat.id, message_app.id)
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

    except:
        all_user = []
    session.close()
    media = MediaGroup()
    caption_text = f"""<a href="{channel_link}">{message_app.chat.title}</a>
Forwarded from <a href="https://t.me/{message_app.forward_from_chat.username}">{message_app.forward_from_chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}"""
    new_caption_for_base = parse_entities(message_app)
    logger.debug(f"Media Group Test Caption Start: {caption_text}")
    if parse_entities(message_app) == "":
        for i in reversed(ls_of_messages):
            logger.debug(f"Media Group Test Caption Iteration: {caption_text}")
            if parse_entities(i) != "":
                caption_text = f"""<a href="{channel_link}">{i.chat.title}</a>
Forwarded from <a href="https://t.me/{message_app.forward_from_chat.username}">{message_app.forward_from_chat.title}</a>
{parse_entities(i)}
{f'<a href="{channel_link}/{i.id}">@</a>' if '+' not in channel_link else ""}"""
                new_caption_for_base = parse_entities(i)
    for ind, i in enumerate(ls_of_messages):

        if ind != 0:
            caption_text = None
        if i.photo is not None:
            try:
                mess_for_bot = await client.send_photo(bot_name, i.photo.file_id)
                # media.attach_photo(InputFile(path),i.caption)
                if message_app.chat.username is None:
                    media.attach_photo(
                        i.photo.file_id, caption=caption_text, parse_mode=ParseMode.HTML
                    )
                else:
                    media.attach_photo(
                        i.photo.file_id, caption=caption_text, parse_mode=ParseMode.HTML
                    )
            except Exception as er:
                path = await client.download_media(i)
                # media.attach_photo(InputFile(path),i.caption)
                if message_app.chat.username is None:
                    media.attach_photo(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
                else:
                    media.attach_photo(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
        if i.video is not None:
            try:
                mess_for_bot = await client.send_video(bot_name, i.video.file_id)
                # media.attach_video(InputFile(path),i.caption)
                if message_app.chat.username is None:
                    media.attach_video(
                        i.video.file_id, caption=caption_text, parse_mode=ParseMode.HTML
                    )
                else:
                    media.attach_video(
                        i.video.file_id, caption=caption_text, parse_mode=ParseMode.HTML
                    )
            except Exception as er:
                path = await client.download_media(i)
                # media.attach_video(InputFile(path),i.caption)
                if message_app.chat.username is None:
                    media.attach_video(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
                else:
                    media.attach_video(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
        if i.document is not None:
            try:
                mess_for_bot = await client.send_document(bot_name, i.document.file_id)
                if message_app.chat.username is None:
                    media.attach_document(
                        i.document.file_id,
                        caption=caption_text,
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    media.attach_document(
                        i.document.file_id,
                        caption=caption_text,
                        parse_mode=ParseMode.HTML,
                    )
            except Exception as er:
                path = await client.download_media(i)
                if message_app.chat.username is None:
                    media.attach_document(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
                else:
                    media.attach_document(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
        if i.audio is not None:
            try:
                mess_for_bot = await client.send_audio(bot_name, i.audio.file_id)
                if i.caption is not None:
                    if message_app.chat.username is None:
                        media.attach_audio(
                            i.audio.file_id,
                            caption=caption_text,
                            parse_mode=ParseMode.HTML,
                        )
                    else:
                        media.attach_audio(
                            i.audio.file_id,
                            caption=caption_text,
                            parse_mode=ParseMode.HTML,
                        )
                else:
                    media.attach_audio(i.audio.file_id)
            except:
                path = await client.download_media(i)
                if message_app.chat.username is None:
                    media.attach_audio(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
                else:
                    media.attach_audio(
                        InputFile(path), caption=caption_text, parse_mode=ParseMode.HTML
                    )
    stop_user_ids = get_double_messages(new_caption_for_base)
    logger.info(f"[{datetime.now()}] Stop_user_id: {stop_user_ids}")
    if check_for_media_group(message_app.chat.id, ls_of_messages[0].id):
        return 0
    actual_all_user = []
    for i in all_user:
        if not (i in stop_user_ids):
            actual_all_user.append(i)
    logger.info(
        f"[{datetime.now()}] Send message in mediagroup with forward. Users: [{actual_all_user}]\n Message entity:\n {str(message_app)}"
    )
    for user in actual_all_user:
        try:
            await bot.send_media_group(
                user,
                media,
            )
        except Exception as er:
            logger.error(f"[{datetime.now()}] Error: {er}")
    session = Session()
    for user in actual_all_user:
        new_message = Message(
            chat_id=message_app.chat.id,
            message_id=message_app.id,
            text=new_caption_for_base,
            user_id=user,
        )
        session.add(new_message)
        session.commit()
    session.close()
