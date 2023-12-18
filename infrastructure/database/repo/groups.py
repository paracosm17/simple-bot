from typing import Literal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User, Profile, Group
from infrastructure.database.repo.base import BaseRepo


class GroupRepo(BaseRepo):
    async def update_or_create_group(
        self,
        group_id: int,
        user_id: int,
        title: str,
        is_forum: bool,
        invite_link: str,
        description: str,
        in_group: bool,
        admin_group: bool
    ):
        insert_stmt = select(Group).from_statement(
            insert(Group)
            .values(
                group_id=group_id,
                user_id=user_id,
                title=title,
                is_forum=is_forum,
                invite_link=invite_link,
                description=description,
                in_group=in_group,
                admin_group=admin_group
            )
            .returning(Group)
            .on_conflict_do_update(
                index_elements=[Group.group_id],
                set_=dict(
                    title=title,
                    is_forum=is_forum,
                    invite_link=invite_link,
                    description=description,
                    in_group=in_group,
                    admin_group=admin_group
                ),
            )
        )
        result = await self.session.scalars(insert_stmt)

        await self.session.commit()
        return result.first()

    async def get_group(self, group_id: int):
        group = await self.session.execute(select(Group).where(Group.group_id == group_id))
        group_scalar: Group = group.scalar()
        if group_scalar is None:
            return False
        return group_scalar

    async def get_owner(self, group_id: int):
        group = await self.session.execute(select(Group).where(Group.group_id == group_id))
        group_scalar: Group = group.scalar()
        if group_scalar is None:
            return False
        return group_scalar.user_id

    async def add_messages_count(self, group_id: int, message_type: Literal["left", "join", "picture"]):
        if message_type not in ["left", "join", "picture"]:
            return False

        group = await self.session.execute(select(Group).where(Group.group_id == group_id))
        group_scalar: Group = group.scalar()
        if group_scalar is None:
            return False

        if message_type == "left":
            group_scalar.left_messages_deleted += 1
        if message_type == "join":
            group_scalar.join_messages_deleted += 1
        if message_type == "picture":
            group_scalar.picture_messages_deleted += 1

        await self.session.commit()
        return True

    async def change_settings(self, group_id: int, message_type: Literal["left", "join", "picture"], boolean: bool):
        if message_type not in ["left", "join", "picture"]:
            return False

        group = await self.session.execute(select(Group).where(Group.group_id == group_id))
        group_scalar: Group = group.scalar()
        if group_scalar is None:
            return False

        if message_type == "left":
            group_scalar.delete_left = boolean
        if message_type == "join":
            group_scalar.delete_join = boolean
        if message_type == "picture":
            group_scalar.delete_pic = boolean

        await self.session.commit()
        return True
