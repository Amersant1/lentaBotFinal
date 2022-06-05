from aiogram.utils.text_decorations import HtmlDecoration
from aiogram.types import MessageEntity
from pyrogram.enums import MessageEntityType

html_decoration = HtmlDecoration()
text = "Купи еще этих французких булок да испанского сыру"
text_entities = [
    MessageEntity(
        "bold",
        3,
        3
    ),
    MessageEntity(
        "italic",
        6,
        10
    )
]
print(html_decoration.unparse(text,text_entities))

