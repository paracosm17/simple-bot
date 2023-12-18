from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Button, ManagedCheckbox

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.profile.states import ProfileStates


async def on_language_selected(c: CallbackQuery,
                               btn: Button,
                               manager: DialogManager):
    repo: RequestsRepo = manager.middleware_data["repo"]
    await repo.users.set_language(manager.event.from_user.id, btn.widget_id)
    await manager.switch_to(ProfileStates.main_menu_state)


async def my_groups_selected(c: CallbackQuery,
                             btn: Button,
                             manager: DialogManager):
    await manager.switch_to(ProfileStates.my_groups_state)


async def add_group_selected(c: CallbackQuery,
                             btn: Button,
                             manager: DialogManager):
    await manager.switch_to(ProfileStates.add_new_group_state)


async def change_language_selected(c: CallbackQuery,
                                   btn: Button,
                                   manager: DialogManager):
    await manager.switch_to(ProfileStates.change_language_state)


async def on_group_selected(callback: CallbackQuery,
                            widget: Any,
                            manager: DialogManager,
                            item_id: str):
    manager.dialog_data["group_id"] = item_id
    await manager.switch_to(ProfileStates.group_settings_state)


async def open_main_menu(c: CallbackQuery,
                         btn: Button,
                         manager: DialogManager):
    await manager.switch_to(ProfileStates.main_menu_state)


async def check_changed_left(event: ChatEvent,
                             checkbox: ManagedCheckbox,
                             manager: DialogManager):
    repo: RequestsRepo = manager.middleware_data["repo"]
    await repo.groups.change_settings(int(manager.dialog_data["group_id"]), message_type="left",
                                      boolean=checkbox.is_checked())


async def check_changed_join(event: ChatEvent,
                             checkbox: ManagedCheckbox,
                             manager: DialogManager):
    repo: RequestsRepo = manager.middleware_data["repo"]
    await repo.groups.change_settings(int(manager.dialog_data["group_id"]), message_type="join",
                                      boolean=checkbox.is_checked())


async def check_changed_picture(event: ChatEvent,
                                checkbox: ManagedCheckbox,
                                manager: DialogManager):
    repo: RequestsRepo = manager.middleware_data["repo"]
    await repo.groups.change_settings(int(manager.dialog_data["group_id"]), message_type="picture",
                                      boolean=checkbox.is_checked())
