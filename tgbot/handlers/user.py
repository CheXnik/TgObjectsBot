from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from tgbot.keyboards import reply

router = Router()


@router.message(CommandStart())
async def user_start(message: Message, bot_state: FSMContext):
    bot_data = await bot_state.get_data()
    start_photo = bot_data.get('start_photo')
    text = f'{html.blockquote(f'{html.italic('Swiss knife in the world of Telegram bot developers 🧠')}')}\n\nBDI©️'

    if start_photo:
        return await message.answer_photo(
            photo=start_photo,
            caption=text,
            reply_markup=reply.get_main_keyboard()
        )

    start_photo = FSInputFile('tgbot/data/start_photo.png')
    send_message = await message.answer_photo(
        photo=start_photo,
        caption=text,
        reply_markup=reply.get_main_keyboard()
    )

    await bot_state.update_data(start_photo=send_message.photo[0].file_id)
