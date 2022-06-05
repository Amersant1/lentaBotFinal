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


@app.on_message(filters.media & filters.channel)
async def echo2(client, message_app):
    stop_user_ids = get_double_messages(message_app.caption)
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
    except:
        all_user = []
    session.close()
    actual_all_user = []
    for i in all_user:
        if not (i in stop_user_ids):
            actual_all_user.append(i)
    logger.info(
        f"[{datetime.now()}] Send message media. Users: [{actual_all_user}]\n Message entity:\n {str(message_app)}"
    )
    if message_app.photo is not None:
        # path = await client.download_media(message_app)
        try:
            mess_for_bot = await client.send_photo(bot_name, message_app.photo.file_id)
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:
                        await bot.send_photo(
                            user,
                            message_app.photo.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_photo(
                            user,
                            message_app.photo.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except Exception as er:
                    logger.error(f"[{datetime.now()}] Error: {er}")
        except Exception as er:
            path = await client.download_media(message_app)
            for user in actual_all_user:
                if message_app.chat.username is None:
                    await bot.send_photo(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                    )
                else:
                    await bot.send_photo(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                    )
            logger.error(f"[{datetime.now()}] Error: {er}")
    if message_app.video is not None:
        try:
            mess_for_bot = await client.send_video(bot_name, message_app.video.file_id)
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:

                        await bot.send_video(
                            user,
                            message_app.video.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_video(
                            user,
                            message_app.video.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except Exception as er:
                    logger.error(f"[{datetime.now()}] Error: {er}")
        except Exception as er:
            logger.error(f"[{datetime.now()}] Error: {er}")
            path = await client.download_media(message_app)
            for user in actual_all_user:
                if message_app.chat.username is None:

                    await bot.send_video(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        supports_streaming=True,
                    )
                else:
                    await bot.send_video(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        supports_streaming=True,
                    )
    if message_app.document is not None:
        try:
            mess_for_bot = await client.send_document(
                bot_name, message_app.document.file_id
            )
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:
                        await bot.send_document(
                            user,
                            message_app.document.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_document(
                            user,
                            message_app.document.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except Exception as er:
                    logger.error(f"[{datetime.now()}] Error: {er}")
        except Exception as er:
            logger.error(f"[{datetime.now()}] Error: {er}")
            path = await client.download_media(message_app)
            for user in actual_all_user:
                if message_app.chat.username is None:
                    await bot.send_document(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                    )
                else:
                    await bot.send_document(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                    )
    if message_app.audio is not None:
        try:
            mess_for_bot = await client.send_audio(bot_name, message_app.audio.file_id)
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:
                        await bot.send_audio(
                            user,
                            message_app.audio.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_audio(
                            user,
                            message_app.audio.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except Exception as er:
                    logger.error(f"[{datetime.now()}] Error: {er}")
        except Exception as er:
            logger.error(f"[{datetime.now()}] Error: {er}")
            path = await client.download_media(message_app)
            for user in actual_all_user:
                if message_app.chat.username is None:
                    await bot.send_audio(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                    )
                else:
                    await bot.send_audio(
                        user,
                        InputFile(path),
                        caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                    )
    if message_app.video_note is not None:
        path = await client.download_media(message_app)
        for user in actual_all_user:
            try:
                if message_app.chat.username is None:
                    await bot.send_video_note(
                        user,
                        InputFile(path),
                    )
                else:
                    await bot.send_video_note(
                        user,
                        InputFile(path),
                    )
            except Exception as er:
                logger.error(f"[{datetime.now()}] Error: {er}")
    if message_app.voice is not None:
        try:
            mess_for_bot = await client.send_voice(bot_name, message_app.voice.file_id)
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:
                        await bot.send_voice(
                            user,
                            message_app.voice.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_voice(
                            user,
                            message_app.voice.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except:
                    pass
        except Exception as er:
            logger.error(f"[{datetime.now()}] Error: {er}")
            path = await client.download_media(message_app)
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:
                        await bot.send_voice(
                            user,
                            InputFile(path),
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_voice(
                            user,
                            InputFile(path),
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except Exception as er:
                    logger.error(f"[{datetime.now()}] Error: {er}")
    if message_app.animation is not None:
        try:
            mess_for_bot = await client.send_animation(
                bot_name, message_app.animation.file_id
            )
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:
                        await bot.send_animation(
                            user,
                            message_app.animation.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_animation(
                            user,
                            message_app.animation.file_id,
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except:
                    pass
        except Exception as er:
            logger.error(f"[{datetime.now()}] Error: {er}")
            path = await client.download_media(message_app)
            for user in actual_all_user:
                try:
                    if message_app.chat.username is None:
                        await bot.send_animation(
                            user,
                            InputFile(path),
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                    else:
                        await bot.send_animation(
                            user,
                            InputFile(path),
                            caption=f"""<a href="{channel_link}">{message_app.chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
                        )
                except Exception as er:
                    logger.error(f"[{datetime.now()}] Error: {er}")
    if message_app.sticker is not None:
        for user in actual_all_user:
            try:
                if message_app.chat.username is None:
                    await bot.send_sticker(
                        user,
                        message_app.sticker.file_id,
                    )
                else:
                    await bot.send_voice(
                        user,
                        message_app.sticker.file_id,
                    )
            except:
                pass
    if message_app.location is not None:

        for user in actual_all_user:
            try:
                if message_app.chat.username is None:
                    await bot.send_location(
                        user,
                        message_app.location.latitude,
                        message_app.location.longitude,
                    )
                else:
                    await bot.send_location(
                        user,
                        message_app.location.latitude,
                        message_app.location.longitude,
                    )
            except Exception as er:
                logger.error(f"[{datetime.now()}] Error: {er}")
    session = Session()
    for user in actual_all_user:
        new_message = Message(
            chat_id=message_app.chat.id,
            message_id=message_app.id,
            text=message_app.caption,
            user_id=user,
        )
        session.add(new_message)
        session.commit()
    session.close()
