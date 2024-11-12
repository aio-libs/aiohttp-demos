from typing import Any

from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker

config = web.AppKey("config", dict[str, Any])
db_pool = web.AppKey("db", async_sessionmaker)
