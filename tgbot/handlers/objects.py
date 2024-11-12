import json

from aiogram import Router, html, F, exceptions
from aiogram.types import BufferedInputFile, Message

from tgbot.keyboards import reply

router = Router()
SHARED_TITLES_TYPES = {
    0: '🎃 User_ID',
    1: '🏠 Chat_ID',
    2: '🤖 Bot_ID',
    3: '📬 Channel_ID'
}


def create_caption(object_info: dict, important_info: list[list] = None) -> tuple:
    important_caption = ''

    if important_info:
        important_caption = '\n'.join([f'{title}: {value}' for title, value in important_info]) + '\n\n'

    caption = html.pre_language(json.dumps(object_info, indent=2, ensure_ascii=False), 'json')

    return caption, important_caption


async def send_object_info(message: Message, important_info: list[list] = None):
    all_info = message.model_dump()
    file = BufferedInputFile(json.dumps(all_info, indent=2).encode(), filename=f'{message.content_type.value}.json')

    object_info = message.model_dump().get(message.content_type)
    caption, important_caption = create_caption(object_info, important_info)

    try:
        await message.reply_document(
            document=file,
            caption=important_caption + caption,
            reply_markup=reply.get_main_keyboard()
        )

    except exceptions.TelegramBadRequest:
        await message.reply_document(
            document=file,
            caption=important_caption,
            reply_markup=reply.get_main_keyboard()
        )


@router.message(F.sticker)
async def get_sticker_object(message: Message):
    important_info = [[html.bold('👁 File_ID'), html.code(message.sticker.file_id)]]

    await send_object_info(message=message, important_info=important_info)


@router.message(F.photo)
async def get_photo_object(message: Message):
    important_info = [[html.bold('👁 File_ID'), html.code(message.photo[-1].file_id)]]

    await send_object_info(message=message, important_info=important_info)


@router.message(F.video)
async def get_video_object(message: Message):
    important_info = [[html.bold('👁 File_ID'), html.code(message.video.file_id)]]

    await send_object_info(message=message, important_info=important_info)


@router.message(F.animation)
async def get_animation_object(message: Message):
    important_info = [[html.bold('👁 File_ID'), html.code(message.animation.file_id)]]

    await send_object_info(message=message, important_info=important_info)


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
    await send_object_info(message=message)
