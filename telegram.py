import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from assets.utils import read_json_from_file
from assets.telegram_module.handlers import start


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(start.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    config_file = read_json_from_file("./config.txt")
    BOT_TOKEN = config_file.get("BOT_TOKEN")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
