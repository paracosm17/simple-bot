from typing import Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User, Profile, Group
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def update_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language_code: str,
        username: Optional[str] = None,
    ):
        insert_stmt = select(User).from_statement(
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                language_code=language_code,
            )
            .returning(User)
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                    language_code=language_code
                ),
            )
        )
        result = await self.session.scalars(insert_stmt)

        await self.session.commit()
        return result.first()

    async def update_or_create_profile(
        self,
        user_id: int
    ):
        insert_stmt = select(Profile).from_statement(
            insert(Profile)
            .values(
                user_id=user_id,
                active=True,
                last_active=datetime.now()
            )
            .returning(Profile)
            .on_conflict_do_update(
                index_elements=[Profile.user_id],
                set_=dict(
                    active=True,
                    last_active=datetime.now()
                ),
            )
        )
        result = await self.session.scalars(insert_stmt)

        await self.session.commit()
        return result.first()

    async def ban_user(self, user_id: int, unban: bool = False):
        profile = await self.session.execute(select(Profile).where(Profile.user_id == user_id))
        profile_scalar: Profile = profile.scalar()

        if profile_scalar is None:
            return False
        if unban:
            profile_scalar.banned = False
        else:
            profile_scalar.banned = True

        await self.session.commit()
        return True

    async def active_user(self, user_id: int, active: bool):
        profile = await self.session.execute(select(Profile).where(Profile.user_id == user_id))
        profile_scalar: Profile = profile.scalar()
        if profile_scalar is None:
            return False
        profile_scalar.active = active
        await self.session.commit()
        return True

    async def check_user(self, user_id: int):
        user = await self.session.execute(select(User).where(User.user_id == user_id))
        user_scalar: User = user.scalar()
        if user_scalar is None:
            return False
        return True

    async def get_user_groups(self, user_id: int):
        profile = await self.session.execute(select(Profile).where(Profile.user_id == user_id))
        profile_scalar: Profile = profile.scalar()
        if profile_scalar is None:
            return False
        groups = await self.session.execute(select(Group).where(Group.user_id == user_id))
        groups_scalar = groups.scalars().all()
        return groups_scalar

    async def set_language(self, user_id: int, language: str):
        profile = await self.session.execute(select(Profile).where(Profile.user_id == user_id))
        profile_scalar: Profile = profile.scalar()
        if profile_scalar is None:
            return False
        profile_scalar.language = language
        await self.session.commit()
        return True

