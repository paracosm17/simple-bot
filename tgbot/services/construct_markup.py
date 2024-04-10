from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def construct_markup(rm: dict | None) -> InlineKeyboardMarkup | None:
    """

    Parameters
    ----------
    rm: dict

    Returns: InlineKeyboardMarkup
    -------

    Чтобы можно было прокидывать InlineKeyboardMarkup через redis, необходимо сериализовать ее в словарь, с помощью
    .model_dump()

    В этой функции сериализованная клавиатура обратно десериализуется в объект InlineKeyboardMarkup
    """
    if rm is None:
        return rm

    for row in rm["inline_keyboard"]:
        for idx, button in enumerate(row):
            row[idx] = InlineKeyboardButton.model_construct(**button)

    return InlineKeyboardMarkup.model_construct(**rm)
