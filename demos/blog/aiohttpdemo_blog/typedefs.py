from typing import Any

from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker

config_key = web.AppKey("config_key", dict[str, Any])
db_key = web.AppKey("db_key", async_sessionmaker)
