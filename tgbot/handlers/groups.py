from aiogram import F
from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.filters import JOIN_TRANSITION, PROMOTED_TRANSITION, LEAVE_TRANSITION
from aiogram.filters import MEMBER, RESTRICTED, LEFT, KICKED, ADMINISTRATOR, CREATOR, IS_NOT_MEMBER
from aiogram.filters import IS_NOT_MEMBER, IS_MEMBER, IS_ADMIN
from aiogram.types import Message, ChatMemberUpdated

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.filters.admin import BotAdminGroupFilter, BotMemberUpdated

group_router = Router()
# group_router.message.filter(F.chat.type.in_({"group", "supergroup"}), BotAdminGroupFilter())
# group_router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))
# group_router.chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@group_router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=PROMOTED_TRANSITION
    ),
    BotMemberUpdated()
)
async def bot_admin(event: ChatMemberUpdated, repo: RequestsRepo):
    await event.bot.send_message(event.from_user.id, f"Бот стал админом в чате {event.chat.title}!")
    await repo.groups.update_or_create_group(
        group_id=event.chat.id,
        user_id=event.from_user.id,
        title=event.chat.title,
        is_forum=event.chat.is_forum or False,
        invite_link=event.chat.invite_link,
        description=event.chat.description,
        in_group=True,
        admin_group=True
    )


@group_router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_MEMBER >> IS_NOT_MEMBER
    ),
    BotMemberUpdated()
)
async def bot_left_from_chat(event: ChatMemberUpdated, repo: RequestsRepo):
    await event.bot.send_message(1657786604, f"Вы выгнали бота из чата {event.chat.title}")
    await repo.groups.update_or_create_group(
        group_id=event.chat.id,
        user_id=event.from_user.id,
        title=event.chat.title,
        is_forum=event.chat.is_forum or False,
        invite_link=event.chat.invite_link,
        description=event.chat.description,
        in_group=False,
        admin_group=False
    )


# NOOOOT WOOOOORK
@group_router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_ADMIN >> (MEMBER | +RESTRICTED)
    ),
    BotMemberUpdated()
)
async def bot_not_admin(event: ChatMemberUpdated, repo: RequestsRepo):
    await event.bot.send_message(1657786604, f"Вы забрали админку у бота в чате {event.chat.title}"
                                                     f"Теперь он не может удалять сервисные сообщения")
    await repo.groups.update_or_create_group(
        group_id=event.chat.id,
        user_id=event.from_user.id,
        title=event.chat.title,
        is_forum=event.chat.is_forum or False,
        invite_link=event.chat.invite_link,
        description=event.chat.description,
        in_group=True,
        admin_group=False
    )


@group_router.message(F.new_chat_members, BotAdminGroupFilter())
async def delete_join(message: Message, repo: RequestsRepo):
    await message.delete()
    await repo.groups.update_or_create_group(
        group_id=message.chat.id,
        user_id=message.from_user.id,
        title=message.chat.title,
        is_forum=message.chat.is_forum or False,
        invite_link=message.chat.invite_link,
        description=message.chat.description,
        in_group=True,
        admin_group=True
    )


@group_router.message(F.left_chat_member, BotAdminGroupFilter())
async def delete_left(message: Message, repo: RequestsRepo):
    await message.delete()
    await repo.groups.update_or_create_group(
        group_id=message.chat.id,
        user_id=message.from_user.id,
        title=message.chat.title,
        is_forum=message.chat.is_forum or False,
        invite_link=message.chat.invite_link,
        description=message.chat.description,
        in_group=True,
        admin_group=True
    )
