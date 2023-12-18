from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Checkbox, Back
from aiogram_dialog.widgets.text import Const, Format

from tgbot.dialogs.profile.getters import generate_my_groups_buttons, get_group
from tgbot.dialogs.profile.selected.profile import on_language_selected, change_language_selected, add_group_selected, \
    my_groups_selected, open_main_menu, on_group_selected, check_changed_left, check_changed_join, check_changed_picture
from tgbot.dialogs.profile.selected.when import profile_exists
from tgbot.dialogs.profile.states import ProfileStates


def language_window():
    return Window(
        Const("Язык"),
        Button(Const("English"), id="en", when=profile_exists, on_click=on_language_selected),
        Button(Const("Русский"), id="ru", when=profile_exists, on_click=on_language_selected),
        state=ProfileStates.language_state
    )


def main_menu_window():
    return Window(
        Const("Главное меню"),
        Button(Const("Мои группы"), id="my_groups", when=profile_exists, on_click=my_groups_selected),
        Button(Const("Добавить группу"), id="add_group", when=profile_exists, on_click=add_group_selected),
        Button(Const("Изменить язык"), id="change_language", when=profile_exists, on_click=change_language_selected),
        state=ProfileStates.main_menu_state,
    )


def my_groups_window():
    return Window(
        Const("Ваши группы"),
        ScrollingGroup(
            Select(
                Format("{item.title} ({item.group_id})"),
                id="s_groups",
                item_id_getter=lambda item: str(item.group_id),
                items="groups",
                on_click=on_group_selected
            ),
            id="my_groups_list",
            width=1,
            height=3,
        ),
        Button(Const("Назад"), on_click=open_main_menu, id="__back__"),
        state=ProfileStates.my_groups_state,
        getter=generate_my_groups_buttons
    )


def add_group_window():
    return Window(
        Const("Тут какая-то подробная инструкция! ДОбавьте бота в группу!"),
        Button(Const("Назад"), on_click=open_main_menu, id="__back__"),
        state=ProfileStates.add_new_group_state
    )


def change_language_window():
    return Window(
        Const("Выберите язык бота"),
        Button(Const("English"), id="eng", when=profile_exists, on_click=on_language_selected),
        Button(Const("Русский"), id="rus", when=profile_exists, on_click=on_language_selected),
        Button(Const("Назад"), on_click=open_main_menu, id="__back__"),
        state=ProfileStates.change_language_state
    )


def group_settings_window():
    return Window(
        Format("Группа {group.title} ({group.group_id})"),
        Checkbox(
            Const("Сообщения о входе удаляются ✅"),
            Const("Сообщения о входе не удаляются ❌"),
            id="set_join",
            default=True,
            on_state_changed=check_changed_join,
        ),
        Checkbox(
            Const("Сообщения о выходе удаляются ✅"),
            Const("Сообщения о выходе не удаляются ❌"),
            id="set_left",
            default=True,
            on_state_changed=check_changed_left,
        ),
        Checkbox(
            Const("Сообщения об изменении картинки удаляются ✅"),
            Const("Сообщения об изменении картинки не удаляются ❌"),
            id="set_pic",
            default=False,
            on_state_changed=check_changed_picture,
        ),
        Back(Const("Назад")),
        getter=get_group,
        state=ProfileStates.group_settings_state
    )
