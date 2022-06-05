import random
import re
from datetime import datetime

import asyncio
from aiogram import Bot, types
from aiogram.types.message import ContentTypes
from aiogram.types import ParseMode
from aiogram.types.input_media import (
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    InputFile,
    MediaGroup,
)
from finder import get_subs_channel

# from client import
from mics import dp, bot, Session, app
from keyboards import *
from texts import *
from databases import ChannelPopular, Report, Subscribe, User, Channel
from states import Form

# from config import channel_id,subs_channel,notification_id


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    session = Session()
    result = session.query(User).filter_by(id=message.chat.id).first()
    if result is None:
        new_user = User(id=message.chat.id, name=message.chat.username)
        session.add(new_user)
        session.commit()
    session.close()
    await message.answer(start_text1)


@dp.message_handler(commands=["find"])
async def send_welcome(message: types.Message):
    await message.answer(find_text, reply_markup=find_keyboard)


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "find_single")
async def remove_channel(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(find_single)
    await Form.AwaitFindSingle.set()


@dp.message_handler(state=Form.AwaitFindSingle)
async def send_welcome(message: types.Message, state):
    if message.text.startswith("@"):
        await message.answer("Подождите, мы ищем похожие каналы...")
        await asyncio.sleep(3)
        try:
            result = get_subs_channel(f"https://tlgrm.ru/channels/{message.text}")[0]
            li = []
            print(get_subs_channel(result))
            [li.append(x) for x in get_subs_channel(result) if x not in li]
            print(li)
            random.shuffle(li)
            print(li)
            links = [
                (f"@{i.split('@')[1]}", f"https://t.me/{i.split('@')[1]}") for i in li
            ]
            await message.answer(
                "Похожие каналы на ваш запрос",
                reply_markup=urls_list(links),
            )
        except Exception as er:
            print(er)
            session = Session()
            all_channels = session.query(ChannelPopular).all()
            random.shuffle(all_channels)
            ls = [
                (i.name, f"https://t.me/{i.name.replace('@','')}") for i in all_channels
            ]
            await message.answer(
                "Мы не смогли найти похожие каналы в нашей базе, предлагаем вам оценить наиболее популярные источники",
                reply_markup=urls_list(ls),
            )
        await state.reset_state()
    else:
        await message.answer("Ошибка! Формат не соотвествуюет необходимому")
        await message.answer(find_text, reply_markup=find_keyboard)


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "find_global")
async def remove_channel(callback_query: types.CallbackQuery):
    session = Session()
    user = session.query(User).filter_by(id=callback_query.message.chat.id).first()
    if len(user.subscribes) < 10:
        await callback_query.message.edit_text(find_global_low)
    else:
        await callback_query.message.edit_text(
            "Подождите, мы анализируем ваши каналы..."
        )
        await asyncio.sleep(3)

        all_channels = session.query(ChannelPopular).all()
        random.shuffle(all_channels)
        ls = [(i.name, f"https://t.me/{i.name.replace('@','')}") for i in all_channels]
        await callback_query.message.edit_text(
            find_global,
            reply_markup=urls_list(ls),
        )


@dp.message_handler(commands=["report"])
async def send_welcome(message: types.Message):
    await Form.AwaitReport.set()
    await message.answer("Отправьте ваше предложение/отзыв", reply_markup=cancel_markup)


@dp.message_handler(text="Отмена", state="*")
async def send_welcome(message: types.Message, state):
    await state.reset_state()
    await message.answer("Главное меню", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.AwaitReport)
async def send_welcome(message: types.Message, state):
    session = Session()
    new_report = Report(text=message.text)
    session.add(new_report)
    session.commit()
    await message.answer("Готово, ваш отзыв оставлен", reply_markup=types.ReplyKeyboardRemove())
    session.close()
    await state.reset_state()


@dp.message_handler(commands="help")
async def send_help(message: types.Message):
    await message.answer(help_text)


@dp.message_handler(commands="list")
async def send_сhannel_list(message: types.Message,state):
    session = Session()
    user = session.query(User).filter_by(id=message.chat.id).first()
    async with state.proxy() as f:
        p = 0
        pag = []
        page = []
        for i in user.subscribes:
            if p > 45:
                pag.append(page)
                page = []
                p = 0
            page.append(i)
            p +=1
        pag.append(page)
    await message.answer("Ваши подписки", reply_markup=channels_list(pag))
    session.close()


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "move")
async def remove_channel(callback_query: types.CallbackQuery,state):
    key = int(callback_query.data.split('~')[1])
    session = Session()
    user = session.query(User).filter_by(id=callback_query.message.chat.id).first()
    p = 0
    pag = []
    page = []
    for i in user.subscribes:
        if p > 45:
            pag.append(page)
            page = []
            p = 0
        page.append(i)
        p +=1
    pag.append(page)
    await callback_query.message.edit_reply_markup(reply_markup=channels_list(pag,key))



@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "remove")
async def remove_channel(callback_query: types.CallbackQuery):
    page_num = int(callback_query.data.split("~")[2])
    key = int(callback_query.data.split("~")[1])
    session = Session()
    session.query(Subscribe).filter_by(id=key).delete()
    session.commit()
    user = session.query(User).filter_by(id=callback_query.message.chat.id).first()
    p = 0
    pag = []
    page = []
    for i in user.subscribes:
        if p > 45:
            pag.append(page)
            page = []
            p = 0
        page.append(i)
        p +=1
    pag.append(page)
    await callback_query.message.edit_text(
        "Ваши подписки", reply_markup=channels_list(pag,page_num)
    )
    session.close()


@dp.message_handler(content_types=ContentTypes.ANY)
async def add_channel(message: types.Message, state):
    if message.forward_from_chat != None:
        session = Session()
        result_channel = (
            session.query(Channel)
            .filter_by(сhannel_id=message.forward_from_chat.id)
            .first()
        )
        if result_channel is None:
            if message.forward_from_chat.username != None:
                new_channels = Channel(
                    сhannel_id=message.forward_from_chat.id,
                    сhannel_name="@" + message.forward_from_chat.username,
                )
                session.add(new_channels)
                session.commit()
            await asyncio.sleep(3)
        result_channel = (
            session.query(Channel)
            .filter_by(сhannel_id=message.forward_from_chat.id)
            .first()
        )
        if result_channel != None:
            result = (
                session.query(Subscribe)
                .filter_by(user_id=message.chat.id, channel_id=result_channel.id)
                .first()
            )
            if result is None:
                new_subscirbe = Subscribe(
                    user_id=message.chat.id, channel_id=result_channel.id
                )
                session.add(new_subscirbe)
                session.commit()
                await message.answer(
                    f"@{message.forward_from_chat.username} {channel_added}"
                )
            else:
                # session.query(Subscribe).filter_by(id=result.id).delete()
                # session.commit()
                await message.answer(
                    f"@{message.forward_from_chat.username} {channel_added_yet}"
                )
        else:
            await message.answer(private_channel)
        session.close()

    elif message.forward_from != None:
        if message.forward_from.id == 5141388392:
            chat_username = message.text.split("\n")[0]
            if chat_username[0] == "@":
                session = Session()
                result_channel = (
                    session.query(Channel).filter_by(сhannel_name=chat_username).first()
                )
                result = (
                    session.query(Subscribe)
                    .filter_by(user_id=message.chat.id, channel_id=result_channel.id)
                    .first()
                )

                if result is None:
                    new_subscirbe = Subscribe(
                        user_id=message.chat.id, channel_id=result_channel.id
                    )
                    session.add(new_subscirbe)
                    session.commit()
                    await message.answer(f"{chat_username} {channel_added}")
                else:
                    # session.query(Subscribe).filter_by(id=result.id).delete()
                    # session.commit()
                    await message.answer(f"{chat_username} {channel_added_yet}")
                session.close()
        else:
            await message.answer(group_add)
    else:
        if message.text is None:
            return 0
        if message.text[0] == "@":
            session = Session()
            result_channel = (
                session.query(Channel).filter_by(сhannel_name=message.text).first()
            )
            if result_channel is None:
                new_channels = Channel(сhannel_name=message.text)
                session.add(new_channels)
                session.commit()
                await asyncio.sleep(3)
            result_channel = (
                session.query(Channel).filter_by(сhannel_name=message.text).first()
            )

            if result_channel != None:
                result = (
                    session.query(Subscribe)
                    .filter_by(user_id=message.chat.id, channel_id=result_channel.id)
                    .first()
                )
                if result is None:
                    new_subscirbe = Subscribe(
                        user_id=message.chat.id, channel_id=result_channel.id
                    )
                    session.add(new_subscirbe)
                    session.commit()
                    await message.answer(f"{message.text} {channel_added}")
                else:
                    # session.query(Subscribe).filter_by(id=result.id).delete()
                    # session.commit()
                    await message.answer(f"{message.text} {channel_added_yet}")
            else:
                await message.answer(f"{mistake}")
            session.close()

        elif message.text[0:13] == "https://t.me/":

            session = Session()
            result_channel = (
                session.query(Channel).filter_by(сhannel_link=message.text).first()
            )
            if result_channel is None:
                new_channels = Channel(
                    сhannel_link=message.text,
                )
                session.add(new_channels)
                session.commit()
                await asyncio.sleep(5)
            result_channel = (
                session.query(Channel).filter_by(сhannel_link=message.text).first()
            )

            if result_channel != None:
                result = (
                    session.query(Subscribe)
                    .filter_by(user_id=message.chat.id, channel_id=result_channel.id)
                    .first()
                )
                if result is None:
                    new_subscirbe = Subscribe(
                        user_id=message.chat.id, channel_id=result_channel.id
                    )
                    session.add(new_subscirbe)
                    session.commit()
                    await message.answer(f"{message.text} {channel_added}")
                else:
                    # session.query(Subscribe).filter_by(id=result.id).delete()
                    # session.commit()
                    await message.answer(f"{message.text} {channel_added_yet}")
            else:
                await message.answer(f"{mistake_link}")
            session.close()
        else:
            await message.answer(not_valid_text)
