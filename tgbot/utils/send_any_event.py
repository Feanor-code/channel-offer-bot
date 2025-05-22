from aiogram import Bot, types


class SendAnyEvent:
    def __init__(
        self, 
        bot: Bot,
        message: types.Message,
        user_id: int,
        reply_markup: types.InlineKeyboardMarkup | None = None
    ) -> None:
        self.bot = bot
        self.message = message
        self.user_id = user_id
        self.reply_markup = reply_markup
        self.event_methods = {
            "photo": (
                bot.send_photo, lambda t: t.photo[0].file_id
            ),
            "video": (
                bot.send_video, lambda t: t.video.file_id
            ),
            "video_note": (
                bot.send_video_note, lambda t: t.video_note.file_id
            ),
            "animation": (
                bot.send_animation, lambda t: t.animation.file_id
            ),
        }
        self.quote_block: str = ""

    def quote(self) -> None:
        if not (text := self.message.caption):
            return 
        
        self.quote_block = f"<blockquote>{text}</blockquote>"

    async def send(self) -> types.Message:
        for event_type, (method, file_id) in self.event_methods.items():
            event = getattr(self.message, event_type, None)

            if event is None:
                continue

            args = {
                "chat_id": self.user_id,
                event_type: file_id(self.message),
                "reply_markup": self.reply_markup
            }

            if event_type != "video_note":
                args["caption"]=self.quote_block

            return await method(**args)
        
        return await self.message.answer("Такое нельзя отправлять :/")
