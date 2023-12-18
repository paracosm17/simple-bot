from aiogram import Router
from aiogram_dialog import DialogManager
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from tgbot.dialogs.profile.states import ProfileStates

profile_router = Router()


@profile_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ProfileStates.language_state)
