from typing import Dict, Union

from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.manager.manager import DialogManager

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models import User, Profile


def profile_exists(data: Dict, widget: Whenable, manager: DialogManager):
    profile: Union[Profile, None] = manager.middleware_data["profile"]
    return bool(profile)


def location_exists(data: Dict, widget: Whenable, manager: DialogManager):
    return manager.dialog_data["birth_long"] or manager.dialog_data["birth_lat"]
