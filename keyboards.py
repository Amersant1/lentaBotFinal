from cgitb import reset
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

main_menu_keyboard.row(
    "Помощь",
    "Список подписок",
)
main_menu_keyboard.row(
    "Как добавить канал",
)
main_menu_keyboard.row(
    "Как отписаться от канала",
)


def channels_list(ls,page_num=0):
    result = InlineKeyboardMarkup()
    if len(ls) == 1:
        for i in ls[0]:
            if i.channel.сhannel_name != None:
                result.row(
                    InlineKeyboardButton(f"{i.channel.сhannel_name}", callback_data="None"),
                    InlineKeyboardButton(f"Удалить", callback_data=f"remove~{i.id}~{page_num}"),
                )
            else:
                result.row(
                    InlineKeyboardButton(
                        f"{i.channel.сhannel_title}", callback_data="None"
                    ),
                    InlineKeyboardButton(f"Удалить", callback_data=f"remove~{i.id}~{page_num}"),
                )
    else:
        for i in ls[page_num]:
            if i.channel is None:
                continue
            if i.channel.сhannel_name != None:
                result.row(
                    InlineKeyboardButton(f"{i.channel.сhannel_name}", callback_data="None"),
                    InlineKeyboardButton(f"Удалить", callback_data=f"remove~{i.id}~{page_num}"),
                )
            else:
                result.row(
                    InlineKeyboardButton(
                        f"{i.channel.сhannel_title}", callback_data="None"
                    ),
                    InlineKeyboardButton(f"Удалить", callback_data=f"remove~{i.id}~{page_num}"),
                )
        result.row(
            InlineKeyboardButton(
                        f"⬅️", callback_data=f"move~{len(ls)-1 if page_num == 0 else page_num-1}"
                    ),
            InlineKeyboardButton(
                        f"{page_num+1}/{len(ls)}", callback_data=f"None"
                    ),
            InlineKeyboardButton(f"➡️", callback_data=f"move~{0 if page_num == len(ls) else page_num+1}"),
                )
    return result


cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_markup.row("Отмена")


find_keyboard = InlineKeyboardMarkup()
find_keyboard.row(
    InlineKeyboardButton("Подобрать похожий канал", callback_data="find_single")
)
find_keyboard.row(
    InlineKeyboardButton("Найти интересные каналы", callback_data="find_global")
)


def urls_list(urls_list):
    result = InlineKeyboardMarkup()
    result.row(InlineKeyboardButton(f"{urls_list[0][0]}", url=f"{urls_list[0][1]}"))
    result.row(InlineKeyboardButton(f"{urls_list[1][0]}", url=f"{urls_list[1][1]}"))
    result.row(InlineKeyboardButton(f"{urls_list[2][0]}", url=f"{urls_list[2][1]}"))
    result.row(InlineKeyboardButton(f"{urls_list[3][0]}", url=f"{urls_list[3][1]}"))
    result.row(InlineKeyboardButton(f"{urls_list[4][0]}", url=f"{urls_list[4][1]}"))
    return result
