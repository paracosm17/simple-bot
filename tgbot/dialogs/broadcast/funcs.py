from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd.button import Button

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.broadcast.states import BroadcastStates
from tgbot.services.broadcaster import broadcast_by_copy
from tgbot.services.construct_markup import construct_markup

broadcast_router = Router()


@broadcast_router.message(Command("broadcast"))
async def start_broadcast(message: Message, dialog_manager: DialogManager, repo: RequestsRepo):
    await dialog_manager.start(BroadcastStates.count_state, data={"users_count": await repo.users.users_count()}, )


async def count_input(m: Message, mi: MessageInput, d: DialogManager):
    repo: RequestsRepo = d.middleware_data["repo"]
    all_users_count = await repo.users.users_count()

    if not m.text.isdigit():
        return
    if int(m.text) > all_users_count:
        return

    d.dialog_data["users_to_send_count"] = int(m.text)
    await d.switch_to(BroadcastStates.random_or_last_state)


async def all_selected(c: CallbackQuery, b: Button, d: DialogManager):
    repo: RequestsRepo = d.middleware_data["repo"]
    d.dialog_data["users_to_send_count"] = await repo.users.users_count()
    d.dialog_data["random"] = False
    await d.switch_to(BroadcastStates.message_state)


async def random_selected(c: CallbackQuery, b: Button, d: DialogManager):
    d.dialog_data["random"] = True
    await d.switch_to(BroadcastStates.message_state)


async def last_selected(c: CallbackQuery, b: Button, d: DialogManager):
    d.dialog_data["random"] = False
    await d.switch_to(BroadcastStates.message_state)


async def message_input(m: Message, mi: MessageInput, d: DialogManager):
    await m.bot.copy_message(chat_id=m.from_user.id, from_chat_id=m.from_user.id,
                             message_id=m.message_id, reply_markup=m.reply_markup)
    d.dialog_data["message_for_send_id"] = m.message_id
    d.dialog_data["message_for_send_reply_markup"] = m.reply_markup.model_dump() if m.reply_markup else None
    await d.switch_to(BroadcastStates.apply_state)


async def send_messages(c: CallbackQuery, b: Button, d: DialogManager):
    await c.message.answer("Запускаю рассылку...")
    repo: RequestsRepo = d.middleware_data["repo"]
    count = await broadcast_by_copy(c.bot,
                                    await repo.users.get_active_users(
                                        d.dialog_data["users_to_send_count"],
                                        random=d.dialog_data.get("random")
                                    ),
                                    c.from_user.id,
                                    d.dialog_data["message_for_send_id"],
                                    construct_markup(d.dialog_data["message_for_send_reply_markup"])
                                    )
    await c.message.answer(f"{count} сообщений разослано!")
    await d.done()
