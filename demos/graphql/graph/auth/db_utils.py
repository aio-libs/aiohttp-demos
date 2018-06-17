from typing import List
from aiopg.sa import SAConnection

from graph.auth.tables import users
from graph.types import RowsProxy
from aiopg.sa.result import RowProxy


__all__ = ['select_users', 'select_user', ]


async def select_users(conn: SAConnection, keys: List[int]) -> RowsProxy:
    cursor = await conn.execute(
        users
            .select()
            .where(users.c.id.in_(keys))
            .order_by(users.c.id)
    )

    return await cursor.fetchall()


async def select_user(conn: SAConnection, key: int) -> RowProxy:
    cursor = await conn.execute(
        users
            .select()
            .where(users.c.id == key)
            .order_by(users.c.id)
    )

    return await cursor.fetchone()
