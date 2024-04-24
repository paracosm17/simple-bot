from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("ban"))
async def ban_user(message: Message, command: CommandObject, repo: RequestsRepo):
    arg = command.args
    if arg and arg.isdigit():
        arg = int(arg)
        if arg > 9223372036854775807:
            await message.reply("Слишком большой id.")
        else:
            banned = await repo.users.ban_user(arg)
            if banned:
                await message.reply("Успешно забанен.")
            else:
                await message.reply("В боте нет такого пользователя.")
    else:
        await message.reply("Введите id пользователя. /ban some_id")


@admin_router.message(Command("bot"))
async def admin_stats(message: Message, repo: RequestsRepo):
    await message.reply(f"""Всего пользователей: {await repo.users.users_count()}
Из них активных: {await repo.users.users_count(only_active=True)}

Активность:
За день: {await repo.users.get_last_active_users_count_by_days(1)}
За неделю: {await repo.users.get_last_active_users_count_by_days(7)}
За месяц: {await repo.users.get_last_active_users_count_by_days(31)}
За год: {await repo.users.get_last_active_users_count_by_days(365)}

Новые пользователи:
За день: {await repo.users.get_new_users_count_by_days(1)}
За неделю: {await repo.users.get_new_users_count_by_days(7)}
За месяц: {await repo.users.get_new_users_count_by_days(31)}
За год: {await repo.users.get_new_users_count_by_days(365)}
""")
