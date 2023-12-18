from aiogram import Router
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import Message, ChatMemberUpdated

from infrastructure.database.repo.requests import RequestsRepo

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Здарова, корова")


@user_router.message(Command("id"))
async def user_id(message: Message):
    await message.reply(f"<code>{message.from_user.id}</code>")


@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, repo: RequestsRepo):
    await repo.users.active_user(event.from_user.id, active=False)


@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, repo: RequestsRepo):
    await repo.users.active_user(event.from_user.id, active=True)
