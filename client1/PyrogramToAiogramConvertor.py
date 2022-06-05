from unittest import result
from aiogram.types import MessageEntity
from pyrogram.enums import MessageEntityType

test_list = [
    {
        "_": "MessageEntity",
        "type": "MessageEntityType.BOLD",
        "offset": 0,
        "length": 50
    },
    {
        "_": "MessageEntity",
        "type": "MessageEntityType.URL",
        "offset": 403,
        "length": 14
    }
]

def convert(PyrogramList):
    case = {
        MessageEntityType.BOLD: "bold",
        MessageEntityType.TEXT_LINK: "text_link",
        MessageEntityType.URL: "url",
        MessageEntityType.ITALIC: "italic",
        MessageEntityType.SPOILER: "spoiler",
        MessageEntityType.CODE : "code",
        MessageEntityType.UNDERLINE : "underline",
        MessageEntityType.STRIKETHROUGH : "strikethrough",
        MessageEntityType.PRE: "pre",
        MessageEntityType.MENTION: "mention",
    }
    result = []
    for i in PyrogramList:
        try:
            result.append(
                MessageEntity(
                    case[i.type],
                    i.offset,
                    i.length,
                    i.url,
                    i.user,
                    i.language
                )
            )
        except Exception as er:
            print(er)
    return result