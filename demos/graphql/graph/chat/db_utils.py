from aiopg.sa import SAConnection as SAConn
from aiopg.sa.result import RowProxy

from graph.types import RowsProxy
from graph.constants import OBJECT_NOT_FOUND_ERROR
from graph.chat.tables import (
    rooms,
    messages,
)


__all__ = [
    'select_rooms',
    'select_messages_by_room_id',
    'select_room',
    'create_message',
    'delete_message',
]


# selects

async def select_rooms(conn: SAConn) -> RowsProxy:
    cursor =  await conn.execute(
        rooms.select().order_by(rooms.c.id)
    )

    return await cursor.fetchall()


async def select_room(conn: SAConn, id: int) -> RowProxy:
    cursor =  await conn.execute(
        rooms.select().where(rooms.c.id == id)
    )
    item = await cursor.fetchone()
    assert item, OBJECT_NOT_FOUND_ERROR

    return  item


async def select_messages_by_room_id(conn: SAConn, room_id: int) -> RowsProxy:
    cursor = await conn.execute(
        messages.select().where(messages.c.room_id == room_id)
    )

    return await cursor.fetchone()


# create

async def create_message(
        conn: SAConn,
        room_id: int,
        owner_id: int,
        body: str,
) -> None:

    await conn.execute(
        messages.insert().values(body=body, owner_id=owner_id, room_id=room_id)
    )


# delete

async def delete_message(conn: SAConn, id: int) -> None:

    await conn.execute(
        messages.delete().where(messages.c.id == id)
    )
