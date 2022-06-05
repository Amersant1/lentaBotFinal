import html
import logging
import re
from html.parser import HTMLParser
from typing import Optional
from typing import TYPE_CHECKING, Generator, List, Optional, Pattern, cast

from pyrogram.enums import MessageEntityType
import utils

# def unparse(text: str, entities: list):
#     text = utils.add_surrogates(text)

#     entities_offsets = []

#     for entity in entities:
#         entity_type = entity.type
#         start = entity.offset
#         end = start + entity.length

#         if entity_type in (MessageEntityType.BOLD, MessageEntityType.ITALIC, MessageEntityType.UNDERLINE,
#                             MessageEntityType.STRIKETHROUGH):
#             name = entity_type.name[0].lower()
#             start_tag = f"<{name}>"
#             end_tag = f"</{name}>"
#         elif entity_type in (MessageEntityType.CODE, MessageEntityType.PRE, MessageEntityType.BLOCKQUOTE,
#                                 MessageEntityType.SPOILER):
#             name = entity_type.name.lower()
#             start_tag = f"<{name}>"
#             end_tag = f"</{name}>"
#         elif entity_type == MessageEntityType.TEXT_LINK:
#             url = entity.url
#             start_tag = f'<a href="{url}">'
#             end_tag = "</a>"
#         elif entity_type == MessageEntityType.TEXT_MENTION:
#             user = entity.user
#             start_tag = f'<a href="tg://user?id={user.id}">'
#             end_tag = "</a>"
#         else:
#             continue

#         entities_offsets.append((start_tag, start,))
#         entities_offsets.append((end_tag, end,))

#     entities_offsets = map(
#         lambda x: x[1],
#             sorted(
#             enumerate(entities_offsets),
#             key=lambda x: (x[1][1], x[0]),
#             reverse=True
#         )

#     )

#     for entity, offset in entities_offsets:
#         text = text[:offset] + entity + text[offset:]

#     return utils.remove_surrogates(text)

def unparse(text: str, entities = None) -> str:
    """
    Unparse message entities
    :param text: raw text
    :param entities: Array of MessageEntities
    :return:
    """
    return "".join(
        _unparse_entities(
            self._add_surrogates(text), sorted(entities, key=lambda item: item.offset) if entities else []
        )
    )

def _unparse_entities(
    text,
    entities,
    offset,
    length,
) -> Generator[str, None, None]:
    if offset is None:
        offset = 0
    length = length or len(text)

    for index, entity in enumerate(entities):
        if entity.offset * 2 < offset:
            continue
        if entity.offset * 2 > offset:
            yield self.quote(self._remove_surrogates(text[offset : entity.offset * 2]))
        start = entity.offset * 2
        offset = entity.offset * 2 + entity.length * 2

        sub_entities = list(
            filter(lambda e: e.offset * 2 < (offset or 0), entities[index + 1 :])
        )
        yield self.apply_entity(
            entity,
            "".join(
                self._unparse_entities(
                    text, sub_entities, offset=start, length=offset
                )
            ),
        )

    if offset < length:
        yield self.quote(self._remove_surrogates(text[offset:length]))


# def validate(text):
#     pool = []
#     for ind,i in enumerate(text):
#         if i == "<" and text[ind+1] != "/":
#             pool.append(text[ind+1])
#         elif i == "<" and text[ind+1] == "/":
#             if i[ind+2] == pool[-1]:
#                 pool.pop(-1)
#             else:
#                 return False
#     return True

# text = """<a href="grem">Text</a>
# <b>bollde</b>"""
# print(validate(text))