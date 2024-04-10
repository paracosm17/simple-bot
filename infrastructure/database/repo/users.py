from datetime import datetime, date, timedelta
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def update_or_create_user(
            self,
            user_id: int,
            full_name: str,
            language_code: str,
            username: Optional[str] = None,
    ):
        insert_user_statement = select(User).from_statement(
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                language_code=language_code,
                active=True,
                last_active=datetime.now()
            )
            .returning(User)
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                    language_code=language_code,
                    active=True,
                    last_active=datetime.now()
                ),
            )
        )
        result = await self.session.execute(insert_user_statement)

        await self.session.commit()
        return result.scalar_one()

    async def ban_user(self, user_id: int):
        user = await self.session.execute(select(User).where(User.user_id == user_id))
        user_scalar: User = user.scalar()
        if user_scalar is None:
            return False
        user_scalar.banned = True
        await self.session.commit()
        return True

    async def unban_user(self, user_id: int):
        user = await self.session.execute(select(User).where(User.user_id == user_id))
        user_scalar: User = user.scalar()
        if user_scalar is None:
            return False
        user_scalar.banned = False
        await self.session.commit()
        return True

    async def active_user(self, user_id: int, active: bool) -> bool:
        user = await self.session.execute(select(User).where(User.user_id == user_id))
        user_scalar: User = user.scalar()
        if user_scalar is None:
            return False
        user_scalar.active = active
        await self.session.commit()
        return True

    async def do_user_exists(self, user_id: int) -> bool:
        user = await self.session.execute(select(User).where(User.user_id == user_id))
        user_scalar: User = user.scalar()
        if user_scalar is None:
            return False
        return True

    async def users_count(self) -> int:
        users = await self.session.execute(select(func.count()).select_from(User))
        return users.scalar()

    async def get_active_users(self, count: int, random: bool = True):
        if random:
            users = await self.session.execute(
                select(User.user_id).where(User.active == True).order_by(func.random()).limit(count)
            )
        else:
            users = await self.session.execute(
                select(User.user_id).where(User.active == True).order_by(User.created_at.desc()).limit(count)
            )
        return users.scalars().all()

    async def get_new_users_today(self) -> int:
        result = await self.session.execute(select(User).filter(
            func.date(User.created_at) == date.today())
        )
        return len(result.scalars().all())

    async def get_new_users_last_7_days(self) -> int:
        result = await self.session.execute(select(User).filter(
            func.date(User.created_at) > date.today() - timedelta(days=7))
        )
        return len(result.scalars().all())
