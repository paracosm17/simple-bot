from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters import BaseFilter
from aiogram.types import Message, ChatMemberUpdated

from tgbot.config import Config
from infrastructure.database.repo.requests import RequestsRepo


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin


class BotMemberUpdated(BaseFilter):
    async def __call__(self, obj: ChatMemberUpdated, config: Config) -> bool:
        return obj.old_chat_member.user.id == obj.bot.id or obj.new_chat_member.user.id == obj.bot.id


class BotAdminGroupFilter(BaseFilter):
    async def __call__(self, obj: Message, config: Config, repo: RequestsRepo) -> bool:
        if obj.new_chat_members:
            for user in obj.new_chat_members:
                if user.id == obj.bot.id:
                    bot_member = await obj.bot.get_chat_member(obj.chat.id, obj.bot.id)
                    if bot_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
                        await obj.bot.send_message(obj.from_user.id, "Бот был добавлен в чат и стал "
                                                                     "администратором!")
                        await repo.groups.update_or_create_group(
                            group_id=obj.chat.id,
                            user_id=obj.from_user.id,
                            title=obj.chat.title,
                            is_forum=obj.chat.is_forum or False,
                            invite_link=obj.chat.invite_link,
                            description=obj.chat.description,
                            in_group=True,
                            admin_group=True
                        )
                        return True
                    else:
                        await obj.bot.send_message(obj.from_user.id, f"Отлично! "
                                                                     f"Бот был добавлен в чат {obj.chat.title}. "
                                                                     f"Теперь сделайте его админом.")
                        await repo.groups.update_or_create_group(
                            group_id=obj.chat.id,
                            user_id=obj.from_user.id,
                            title=obj.chat.title,
                            is_forum=obj.chat.is_forum or False,
                            invite_link=obj.chat.invite_link,
                            description=obj.chat.description,
                            in_group=True,
                            admin_group=False
                        )
                        return False
        try:
            bot_member = await obj.bot.get_chat_member(obj.chat.id, obj.bot.id)
            return bot_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
        except:
            return False
