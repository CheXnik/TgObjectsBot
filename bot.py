import asyncio
import logging

import betterlogging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares.custom import CustomMiddleware


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='🔰 Main menu'),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


def register_global_middlewares(dp: Dispatcher, config: Config, bot_state: FSMContext):
    middleware_types = [
        CustomMiddleware(config, 'config'),
        CustomMiddleware(bot_state, 'bot_state')
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    betterlogging.basic_colorized_config(level=logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting bot.')


async def main():
    setup_logging()

    config = load_config('.env')
    storage = MemoryStorage()

    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=config.tg_bot.token, default=default)
    bot_state = FSMContext(storage=storage, key=StorageKey(chat_id=bot.id, user_id=bot.id, bot_id=bot.id))
    dp = Dispatcher(storage=storage)

    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config, bot_state)

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logging.warning('The bot was stopped.')
