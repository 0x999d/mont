import routes
from loader import (
    DBAdapter, 
    app,
    HTTPScanner
)
from threading import Thread


async def main() -> None:
    await DBAdapter.init_tables()
    Thread(target=HTTPScanner.start, daemon=True).start()
    # Thread для предотвращения нехватки времени для io задач

app.add_event_handler(event_type="startup", func=main)

app.include_router(routes.users.router)
app.include_router(routes.urls.router)
app.include_router(routes.history.router)