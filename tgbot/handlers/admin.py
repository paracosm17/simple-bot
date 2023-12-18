from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter
from infrastructure.database.repo.requests import RequestsRepo

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
