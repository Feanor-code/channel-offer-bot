import asyncio

import logging

from tgbot.handlers.edit_post import router
from .dispatcher import bot, dp

logging = logging.getLogger(__name__)


async def on_startup() -> None:
    pass
    

async def main() -> None:
    dp.include_routers(router)
    dp.startup.register(on_startup)

    # await bot.delete_webhook(drop_pending_updates=True) :: наверное, лучше включить
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
