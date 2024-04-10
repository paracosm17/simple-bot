from aiogram import types, Router, F
from aiogram.utils.markdown import hcode

echo_router = Router()


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message):
    text = [
        "Эхо.",
        hcode(message.text),
    ]
    await message.answer("\n".join(text))
