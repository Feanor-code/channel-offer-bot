from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram import types

from tgbot.dispatcher import bot
from tgbot.utils.send_any_event import SendAnyEvent


class EventMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Update, Dict[str, Any]], Awaitable[Any]],
        event: types.Update,
        data: Dict[str, Any]
    ) -> Any:
        message = None
        if event.message:
            message = event.message 
        if event.callback_query:
            message = event.callback_query.message
        
        data["any_event"] = SendAnyEvent(
            bot=bot,
            message=message
        )
        return await handler(event, data)
