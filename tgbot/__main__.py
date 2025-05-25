import asyncio

import logging

from tgbot.handlers.edit_post import router
from .dispatcher import bot, dp


async def main() -> None:
    dp.include_routers(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    # await bot.delete_webhook(drop_pending_updates=True) :: наверное, лучше включить


if __name__ == "__main__":
    asyncio.run(main())
