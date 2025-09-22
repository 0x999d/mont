from asyncio import run, gather
from loader import dp, APIClient, bot

from notifier import Notify
import handlers


NotifyManager = Notify(api=APIClient)

async def main() -> None:
    await APIClient.init_tables()

    coro = NotifyManager.start()
    await gather(*[
        coro,
        dp.start_polling(bot)
    ])

if __name__ == "__main__":
    run(main())