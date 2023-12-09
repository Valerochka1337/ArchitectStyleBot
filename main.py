import asyncio
import logging
import sys

from bot.RandomQuiz.random_quiz import *
from bot.handlers.quiz_handlers import *


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
