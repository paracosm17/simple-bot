from aiogram_dialog import Dialog

from tgbot.dialogs.broadcast import windows


def broadcast_dialogs():
    return [
        Dialog(
            windows.broadcast_users_count_window(),
            windows.random_or_last_window(),
            windows.message_window(),
            windows.apply_window(),
        )
    ]
