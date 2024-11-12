from aiogram.types import KeyboardButton, KeyboardButtonRequestChat,KeyboardButtonRequestUsers
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard():
    request_user = KeyboardButton(
        text='User info 🎃',
        request_users=KeyboardButtonRequestUsers(
            request_id=0,
            user_is_bot=False,
            request_photo=True,
            request_username=True,
            request_name=True,
            request_chat=True,
            max_quantity=1
        )
    )
    request_chat = KeyboardButton(
        text='Chat info 🏠',
        request_chat=KeyboardButtonRequestChat(
            request_id=1,
            chat_is_channel=False,
            request_title=True,
            request_photo=True,
            request_username=True
        )
    )
    request_bot = KeyboardButton(
        text='Bot info 🤖',
        request_users=KeyboardButtonRequestUsers(
            request_id=2,
            user_is_bot=True,
            request_photo=True,
            request_username=True,
            request_name=True,
            request_chat=True,
            max_quantity=1
        )
    )
    request_channel = KeyboardButton(
        text='Channel info 📬',
        request_chat=KeyboardButtonRequestChat(
            request_id=3,
            chat_is_channel=True,
            request_title=True,
            request_photo=True,
            request_username=True
        )
    )

    return ReplyKeyboardBuilder().row(
        request_user, request_chat,
        request_bot, request_channel,
        width=2
    ).as_markup(resize_keyboard=True)
