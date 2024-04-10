import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs

from infrastructure.database.setup import create_session_pool, create_postgres_engine, create_metadata
from tgbot.config import load_config, Config
from tgbot.dialogs.broadcast import broadcast_dialogs
from tgbot.dialogs.broadcast.funcs import broadcast_router
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.services import broadcaster


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот запущен")


async def webhook(bot: Bot):
    await bot.set_webhook(f"https://domain.ru/webhook")


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool, engine):
    middleware_types = [
        ConfigMiddleware(config),
        DatabaseMiddleware(session_pool, engine),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.chat_member.outer_middleware(middleware_type)
        dp.my_chat_member.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    bl.basic_colorized_config(level=logging.ERROR)

    logging.basicConfig(
        level=logging.ERROR,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Бот запущен")


def get_storage(config):
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher(storage=storage)

    engine = create_postgres_engine(config.db)
    session_pool = create_session_pool(engine)
    async with engine.begin() as conn:
        await conn.run_sync(create_metadata())

    dp.include_routers(broadcast_router, *broadcast_dialogs())
    setup_dialogs(dp)
    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config, session_pool, engine)

    await on_startup(bot, config.tg_bot.admin_ids)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен")
