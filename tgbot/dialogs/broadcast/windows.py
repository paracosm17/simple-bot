from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Format, Const

from tgbot.dialogs.broadcast.funcs import count_input, all_selected, send_messages, message_input, random_selected, \
    last_selected
from tgbot.dialogs.broadcast.states import BroadcastStates


def broadcast_users_count_window():
    return Window(
        Format('Скольким людям сделать рассылку? Выберите всем активным ({start_data[users_count]}) '
               'или введите свое число'),
        Button(text=Format("Всем активным ({start_data[users_count]})"), id="allbroadcast", on_click=all_selected),
        MessageInput(func=count_input),
        Cancel(Const("Отмена")),
        state=BroadcastStates.count_state,
    )


def random_or_last_window():
    return Window(
        Const('Каким пользователям разослать?'),
        Button(text=Format("Рандомным {dialog_data[users_to_send_count]} пользователям"), id="rand",
               on_click=random_selected),
        Button(text=Format("Последним {dialog_data[users_to_send_count]} пользователям"), id="last",
               on_click=last_selected),
        Cancel(Const("Отмена")),
        state=BroadcastStates.random_or_last_state,
    )


def message_window():
    return Window(
        Const('Отправьте сообщение, которое необходимо разослать'),
        Cancel(Const("Отмена")),
        MessageInput(func=message_input),
        state=BroadcastStates.message_state,
    )


def apply_window():
    return Window(
        Format('Разослать это сообщение {dialog_data[users_to_send_count]} пользователям?'),
        Button(text=Const("Разослать"), id="go", on_click=send_messages),
        Cancel(Const("Отмена")),
        state=BroadcastStates.apply_state,
    )
