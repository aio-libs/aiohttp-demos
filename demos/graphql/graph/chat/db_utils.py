from aiopg.sa import SAConnection as SAConn

from graph.types import RowsProxy
from graph.chat.tables import (
    rooms,
    messages,
)


__all__ = ['select_rooms', 'select_messages_by_room_id', ]


async def select_rooms(conn: SAConn) -> RowsProxy:
    cursor =  await conn.execute(
        rooms.select().order_by(rooms.c.id)
    )

    return await cursor.fetchall()


async def select_messages_by_room_id(conn: SAConn, room_id: int) -> RowsProxy:
    cursor = await conn.execute(
        messages.select().where(messages.c.room_id == room_id)
    )

    return await cursor.fetchall()
