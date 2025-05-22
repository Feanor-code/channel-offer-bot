from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from tgbot.config import config
from tgbot.keyboards.callbacks import ConfirmCallback
from tgbot.keyboards.keyboards import confirm_button
from tgbot.utils.send_any_event import SendAnyEvent

router = Router()


@router.message()
async def edit_post(message: types.Message, bot: Bot, state: FSMContext) -> None:
    any_event = SendAnyEvent(
        bot,
        message,
        config.owner.id,
        await confirm_button()
    )
    any_event.quote()
    any_event.quote_block = any_event.quote_block + config.owner.post_text
    await any_event.send()

    await state.update_data(any_event=any_event)


@router.callback_query(ConfirmCallback())
async def confirm(query: types.CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    any_event: SendAnyEvent = data.get("any_event")

    if any_event is None:
        return
    
    any_event.user_id = config.bot.channel_id
    any_event.reply_markup = None
    await any_event.send()
