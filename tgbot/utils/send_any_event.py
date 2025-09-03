from __future__ import annotations
import typing

from tgbot.config import config

if typing.TYPE_CHECKING:
    from aiogram import Bot    
    from aiogram import types


class SendAnyEvent:
    def __init__(
        self, 
        bot: Bot,
        message: types.Message,
        reply_markup: types.InlineKeyboardMarkup | None = None
    ) -> None:
        self.message = message
        self.user_id = config.owner.id
        self.reply_markup = reply_markup
        self.event_methods = {
            "photo": (bot.send_photo, lambda t: t.photo[0].file_id),
            "video": (bot.send_video, lambda t: t.video.file_id),
            "video_note": (bot.send_video_note, lambda t: t.video_note.file_id),
            "animation": (bot.send_animation, lambda t: t.animation.file_id)
        }
        self.quote_block: str = ""

    def type_check(self) -> tuple[str, typing.Any, typing.Any] | None:
        for event_type, (method, file_id) in self.event_methods.items():
           event = getattr(self.message, event_type, None)

           if event is None:
               continue

           return event_type, method, file_id

    def quote(self) -> None:
        if (text := self.message.caption) is None:
            return None 
        
        self.quote_block = f"<blockquote>{text}</blockquote>"

    async def send(self) -> types.Message | None:
        if (event := self.type_check()) is None:
            return None
        
        event_type, method, file_id = event

        args = {
             "chat_id": self.user_id,
             event_type: file_id(self.message),
             "reply_markup": self.reply_markup
         }
       
        if event_type != "video_note":
             args["caption"]=self.quote_block
       
        return await method(**args)
