import asyncio
import logging
from typing import Union

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import InlineKeyboardMarkup


async def send_message(
        bot: Bot,
        user_id: Union[int, str],
        text: str,
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    try:
        await bot.send_message(
            user_id,
            text,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
        )
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            bot, user_id, text, disable_notification, reply_markup
        )
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast(
        bot: Bot,
        users: list[Union[str, int]],
        text: str,
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
) -> int:
    count = 0
    try:
        for user_id in users:
            if await send_message(
                    bot, user_id, text, disable_notification, reply_markup
            ):
                count += 1
            await asyncio.sleep(
                0.05
            )
    finally:
        logging.info(f"{count} сообщений разослано")

    return count


async def send_message_by_copy(
        bot: Bot,
        user_id: int,
        from_user_id: int,
        message_id: int,
        reply_markup: InlineKeyboardMarkup | None
) -> bool:
    try:
        await bot.copy_message(
            user_id,
            from_user_id,
            message_id,
            reply_markup=reply_markup
        )
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message_by_copy(bot, user_id, from_user_id, message_id, reply_markup)
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast_by_copy(
        bot: Bot,
        users: list[Union[str, int]],
        from_user_id: int,
        message_id: int,
        reply_markup: InlineKeyboardMarkup | None
) -> int:
    count = 0
    try:
        for user_id in users:
            if await send_message_by_copy(bot, user_id, from_user_id, message_id, reply_markup):
                count += 1
            await asyncio.sleep(
                0.05
            )
    finally:
        logging.info(f"{count} сообщений разослано")

    return count
