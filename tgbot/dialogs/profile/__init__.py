from aiogram_dialog import Dialog
from tgbot.dialogs.profile import windows


def profile_dialogs():
    return [
        Dialog(
            windows.language_window(),
            windows.main_menu_window(),
            windows.my_groups_window(),
            windows.group_settings_window(),
            windows.add_group_window(),
            windows.change_language_window(),
            on_close=...
        )
    ]
