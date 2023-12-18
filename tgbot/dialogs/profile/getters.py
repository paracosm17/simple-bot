from aiogram_dialog import DialogManager
from infrastructure.database.repo.requests import RequestsRepo


async def generate_my_groups_buttons(dialog_manager: DialogManager, **kwargs):
    repo: RequestsRepo = dialog_manager.middleware_data["repo"]
    groups = await repo.users.get_user_groups(dialog_manager.middleware_data["user"].user_id)
    return {"groups": groups}


async def get_group(dialog_manager: DialogManager, **kwargs):
    repo: RequestsRepo = dialog_manager.middleware_data["repo"]
    group = await repo.groups.get_group(int(dialog_manager.dialog_data["group_id"]))
    return {"group": group}
