from aiogram import types

from .callbacks import ConfirmCallback
from .keyboards_builder import inline_button


async def confirm_button() -> types.InlineKeyboardMarkup:
    confirm = ConfirmCallback().pack()
    return await inline_button("Выложить 🔗", confirm)
