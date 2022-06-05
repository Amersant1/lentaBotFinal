import asyncio
from datetime import datetime
from email import message
from re import I
import sys

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
logging.basicConfig(filename="sample.log", level=logging.INFO)

service_bot = bot_name

def parse_entities(message_app):
    # print(message_app.entities, message_app.caption_entities)
    # print(message_app.text, message_app.caption)
    # print(dir(message_app.entities[0]),type(message_app.entities[0]))
    if message_app.entities is not None:
        try:
            aiogram_entities = convert(message_app.entities)
            html_decoration = HtmlDecoration()
            depars = html_decoration.unparse(message_app.text, aiogram_entities)
            print(depars)
            return depars 
        except Exception as er:
            print(er)
            return message_app.text
    elif message_app.caption_entities is not None:
        try:
            aiogram_entities = convert(message_app.caption_entities)
            html_decoration = HtmlDecoration()
            depars = html_decoration.unparse(message_app.caption, aiogram_entities)
            print(depars)
            return depars 
        except Exception as er:
            print(er)
            return message_app.caption
    else:
        if message_app.text is not None:
            return message_app.text
        elif message_app.caption is not None:
            return message_app.caption
        else:
            print(None)
            return ""


def check_сhannels():

    session = Session()
    all_сhannel = session.query(Channel).filter_by(subscription=False).all()
    for сhannel in all_сhannel:
        if сhannel.сhannel_name != None:
            try:
                app.join_chat(сhannel.сhannel_name)
            except:
                session.query(Channel).filter_by(id=сhannel.id).delete()
                session.commit()
                сhannel = None
            if сhannel != None:
                chat_inf = app.get_chat(сhannel.сhannel_name)
                session.query(Channel).filter_by(
                    сhannel_name=сhannel.сhannel_name
                ).update({"subscription": True})
                session.commit()
                session.query(Channel).filter_by(
                    сhannel_name=сhannel.сhannel_name
                ).update({"сhannel_id": chat_inf.id})
                session.commit()
                session.query(Channel).filter_by(
                    сhannel_name=сhannel.сhannel_name
                ).update({"сhannel_link": "https://t.me/" + сhannel.сhannel_name[1:]})

                session.commit()

        elif сhannel.сhannel_link != None:
            try:
                try:
                    print(сhannel.сhannel_link.split("chat/"))
                    if "+" in сhannel.сhannel_link:
                        print(True)
                        app.join_chat(сhannel.сhannel_link)
                    else:
                        app.join_chat(сhannel.сhannel_link.split("/")[-1])
                except Exception as er:
                    print(er)
                    session.query(Channel).filter_by(id=сhannel.id).delete()
                    session.commit()
                    сhannel = None
                if сhannel != None:
                    chat_inf = app.get_chat(сhannel.сhannel_link)
                    session.query(Channel).filter_by(
                        сhannel_link=сhannel.сhannel_link
                    ).update({"subscription": True})
                    session.commit()
                    session.query(Channel).filter_by(
                        сhannel_link=сhannel.сhannel_link
                    ).update({"сhannel_id": chat_inf.id})
                    session.commit()
                    session.query(Channel).filter_by(
                        сhannel_link=сhannel.сhannel_link
                    ).update({"сhannel_title": chat_inf.title})
                    session.commit()

            except:
                session.query(Channel).filter_by(
                    сhannel_link=сhannel.сhannel_link
                ).update({"сhannel_name": "@" + сhannel.сhannel_link[13:]})
                session.commit()
    session.close()

@app.on_message(filters.forwarded & filters.text)
async def echo(client, message_app):
    session = Session()
    if (
        session.query(Message)
        .filter_by(chat_id=message_app.chat.id, message_id=message_app.id)
        .first()
        is not None
    ):
        return 0
    if message_app.text is not None:
        if session.query(Message).filter_by(text=message_app.text).first() is not None:
            return 0
    new_message = Message(
        chat_id=message_app.chat.id,
        message_id=message_app.id,
        text=message_app.text,
    )
    session.add(new_message)
    session.commit()
    session.close()
    session = Session()
    try:
        channel_link = (
            session.query(Channel)
            .filter_by(сhannel_id=message_app.chat.id)
            .first()
            .get_link()
        )
    except Exception as er:
        logging.error(f"[{datetime.now()}] Error: {er}")
        return 0
    try:
        all_user = (
            session.query(Channel)
            .filter_by(сhannel_id=message_app.chat.id)
            .first()
            .subs
        )
        all_user = [i.user_id for i in all_user]

    except Exception as er:
        logging.error(f"[{datetime.now()}] Error: {er}")
        all_user = []
    logging.info(
        f"[{datetime.now()}] Send message in text with forward. Message entity:\n {str(message_app)}"
    )
    for user in all_user:
        try:
            await bot.send_message(
                user,
                f"""<a href="{channel_link}">{message_app.chat.title}</a>
Forwarded from <a href="https://t.me/{message_app.forward_from_chat.username}">{message_app.forward_from_chat.title}</a>
{parse_entities(message_app)}
{f'<a href="{channel_link}/{message_app.id}">@</a>' if '+' not in channel_link else ""}""",
            )
        except Exception as er:
            logging.error(f"[{datetime.now()}] Error: {er}")
    session.close()