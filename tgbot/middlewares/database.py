from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from infrastructure.database.models.users import User
from infrastructure.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool, engine):
        self.session_pool = session_pool
        self.engine = engine

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)

            if not event.from_user.is_bot:
                user: User = await repo.users.update_or_create_user(
                    user_id=event.from_user.id,
                    full_name=event.from_user.full_name,
                    language_code=event.from_user.language_code,
                    username=event.from_user.username
                )

                if user.banned:
                    await event.answer("Вы заблокированы в боте.")
                    return

                data["user"] = user

            data["session"] = session
            data["engine"] = self.engine
            data["repo"] = repo

            result = await handler(event, data)

        return result
