import json
import logging
from typing import List, Dict

from aiogram import Router, html, F
from aiogram.types import Message

from tgbot.keyboards import reply

router = Router()
logger = logging.getLogger(__name__)

SHARED_TITLES_TYPES = {
    0: '🎃 User_ID',
    1: '🏠 Chat_ID',
    2: '🤖 Bot_ID',
    3: '📬 Channel_ID'
}


def create_caption(object_info: Dict, important_info: List[List] = None) -> tuple:
    important_caption = ''

    if important_info:
        important_caption = '\n'.join([f'{title}: {value}' for title, value in important_info]) + '\n\n'

    caption = html.pre_language(json.dumps(object_info, indent=2, ensure_ascii=False), 'json')

    return caption, important_caption


async def send_object_info(message: Message, important_info: List[List] = None):
    object_info = message.model_dump().get(message.content_type)
    caption, important_caption = create_caption(object_info, important_info)

    await message.reply(
        text=important_caption + caption,
        reply_markup=reply.get_main_keyboard()
    )


@router.message(F.users_shared)
async def get_user_object(message: Message):
    important_info = [
        [
            html.bold(SHARED_TITLES_TYPES.get(message.users_shared.request_id)),
            html.code(message.users_shared.users[0].user_id)
        ]
    ]

    await send_object_info(message=message, important_info=important_info)


@router.message(F.chat_shared)
async def get_chat_object(message: Message):
    important_info = [
        [
            html.bold(SHARED_TITLES_TYPES.get(message.chat_shared.request_id)),
            html.code(message.chat_shared.chat_id)
        ]
    ]

    await send_object_info(message=message, important_info=important_info)


@router.message()
async def get_other_objects(message: Message):
    if message.photo:
        important_info = [[html.bold('👁 File_ID'), html.code(message.photo[-1].file_id)]]

    elif message.video:
        important_info = [[html.bold('👁 File_ID'), html.code(message.video.file_id)]]

    elif message.document:
        important_info = [[html.bold('👁 File_ID'), html.code(message.document.file_id)]]

    elif message.audio:
        important_info = [[html.bold('👁 File_ID'), html.code(message.audio.file_id)]]

    elif message.voice:
        important_info = [[html.bold('👁 File_ID'), html.code(message.voice.file_id)]]

    elif message.video_note:
        important_info = [[html.bold('👁 File_ID'), html.code(message.video_note.file_id)]]

    elif message.animation:
        important_info = [[html.bold('👁 File_ID'), html.code(message.animation.file_id)]]

    elif message.sticker:
        important_info = [[html.bold('👁 File_ID'), html.code(message.sticker.file_id)]]

    else:
        important_info = [
            [html.bold('👁 BOT HTML'), html.code(html.quote(message.html_text))],
            [
                html.bold('👁 USER HTML'),
                html.code(html.quote(message.html_text.replace('tg-emoji', 'emoji').replace('emoji-id', 'id')))
            ]
        ]

    await send_object_info(message=message, important_info=important_info)
