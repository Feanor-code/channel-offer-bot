from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_keyboard(
    buttons: tuple[str, str] | list[dict[str, str]], adjust: tuple[int, ...] = (1,)
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for button in buttons:
        if isinstance(button, dict):
            builder.button(**button)
        elif isinstance(button, tuple):
            text, callback_data = button
            builder.button(text=text, callback_data=callback_data)
        else:
            raise ValueError(f"Unknown button type: {button}")
    
    builder.adjust(*adjust)
    return builder.as_markup()


async def inline_button(
    text: str, 
    callback_data: str | None = None, 
    url: str | None = None
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if callback_data:
        builder.row(
            types.InlineKeyboardButton(text=text, callback_data=callback_data)
        )
    
    if url:
        builder.row(
            types.InlineKeyboardButton(text=text, url=url)
        )

    return builder.as_markup()
