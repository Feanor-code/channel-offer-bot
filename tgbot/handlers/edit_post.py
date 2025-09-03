from __future__ import annotations
import typing 

from aiogram import Router

from tgbot.config import config
from tgbot.keyboards.callbacks import ConfirmCallback
from tgbot.keyboards.keyboards import confirm_button

if typing.TYPE_CHECKING:
    from aiogram import types
    from tgbot.utils.send_any_event import SendAnyEvent

router = Router()


@router.message()
async def edit_post(message: types.Message, any_event: SendAnyEvent) -> None:
    any_event.quote(highlight=True)
    any_event.quote_block = any_event.quote_block + config.owner.post_text
    any_event.reply_markup = await confirm_button()

    if await any_event.send() is None:
        await message.reply(
            "Такое отправлять нельзя! 🚫 / You can't send this! 🚫\n\n"
            "Пожалуйста, отправь фото, видео, кружок или GIF.\n"
            "Please send a photo, video, voice message, or GIF."
        )


@router.callback_query(ConfirmCallback())
async def confirm(query: types.CallbackQuery, any_event: SendAnyEvent) -> None: 
    await query.message.delete_reply_markup()

    any_event.quote()
    any_event.user_id = config.bot.channel_id
    any_event.reply_markup = None
    await any_event.send()
