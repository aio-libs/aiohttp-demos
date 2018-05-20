from aiopg.sa import SAConnection
from aiopg.sa.result import ResultProxy

from graph.chat.tables import rooms


__all__ = ['select_rooms', ]


async def select_rooms(conn: SAConnection) -> ResultProxy:
    cursor =  await conn.execute(
        rooms.select().order_by(rooms.c.id)
    )

    return await cursor.fetchall()
