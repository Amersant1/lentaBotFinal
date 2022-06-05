import re
from struct import unpack
import sys

sys.path.append("../")
from pyrogram import Client, filters
from pyrogram.parser import Parser
from mics import dp, bot, app, Session
from databases import MediaGroupInfo, Message, User, Channel, Subscribe
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
from PyrogramToAiogramConvertor import convert
from aiogram.utils.text_decorations import HtmlDecoration
from loguru import logger

# SMP = Supplementary Multilingual Plane: https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview
SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")


def add_surrogates(text):
    # Replace each SMP code point with a surrogate pair
    return SMP_RE.sub(
        lambda match: "".join(  # Split SMP in two surrogates
            chr(i) for i in unpack("<HH", match.group().encode("utf-16le"))
        ),
        text,
    )


def remove_surrogates(text):
    # Replace each surrogate pair with a SMP code point
    return text.encode("utf-16", "surrogatepass").decode("utf-16")


def replace_once(source: str, old: str, new: str, start: int):
    return source[:start] + source[start:].replace(old, new, 1)


def get_double_messages(text):
    session = Session()
    if text is None or text == "":
        return []
    ls_stop_ids = [
        i.user_id
        for i in session.query(Message).filter_by(text=text).all()
        if i.user_id is not None
    ]
    session.close()
    return ls_stop_ids


def check_for_media_group(message_id, chat_id):
    session = Session()
    message = (
        session.query(MediaGroupInfo)
        .filter_by(message_id=message_id, chat_id=chat_id)
        .first()
    )
    if message is None:
        trigger = False
    else:
        trigger = True
    print(trigger)
    new_media_group = MediaGroupInfo(message_id=message_id, chat_id=chat_id)
    session.add(new_media_group)
    session.commit()
    session.close()
    return trigger


def check_message_in_base(message_app):
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
            return False
    new_message = Message(
        chat_id=message_app.chat.id,
        message_id=message_app.id,
        text=message_app.text,
    )
    session.add(new_message)
    session.commit()
    session.close()
    return True


def parse_entities(message_app):
    if message_app.entities is not None:
        try:
            aiogram_entities = convert(message_app.entities)
            html_decoration = HtmlDecoration()
            depars = html_decoration.unparse(message_app.text, aiogram_entities)
            logger.info(f"Result in parse_entities text_entities: {depars}")
            return depars
        except Exception as er:
            logger.error(f"Error in parse_entities: {er}")
            return message_app.text
    elif message_app.caption_entities is not None:
        try:
            aiogram_entities = convert(message_app.caption_entities)
            html_decoration = HtmlDecoration()
            depars = html_decoration.unparse(message_app.caption, aiogram_entities)
            logger.info(f"Result in parse_entities caption_entities: {depars}")
            return depars
        except Exception as er:
            logger.error(f"Error in parse_entities: {er}")
            return message_app.caption
    else:
        if message_app.text is not None:
            return message_app.text
        elif message_app.caption is not None:
            return message_app.caption
        else:
            logger.error(f"Error in parse_entities: Return None")
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

        """elif сhannel.сhannel_id != None:
            chat_inf = app.get_chat(сhannel.сhannel_id)
            if chat_inf.username != None:
                session.query(Channel).filter_by(
                    сhannel_name=сhannel.сhannel_name
                ).update({"сhannel_name": "@" + chat_inf.username})
                session.commit()
                app.join_chat("@" + chat_inf.username)
                session.query(Channel).filter_by(сhannel_id=сhannel.сhannel_id).update(
                    {"subscription": True}
                )
                session.commit()"""
    session.close()
