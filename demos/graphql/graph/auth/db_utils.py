from typing import List
from aiopg.sa import SAConnection
from aiopg.sa.result import ResultProxy

from graph.auth.tables import users


__all__ = ['select_users', ]


async def select_users(conn: SAConnection, keys: List[int]) -> ResultProxy:
    cursor = await conn.execute(
        users
            .select()
            .where(users.c.id.in_(keys))
            .order_by(users.c.id)
    )

    return await cursor.fetchall()
