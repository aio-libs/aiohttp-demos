from graph.chat.models import Message, Room
from graph.constants import OBJECT_NOT_FOUND_ERROR
from sqlalchemy.sql import select

__all__ = [
    "select_rooms",
    "select_messages_by_room_id",
    "select_room",
    "create_message",
    "delete_message",
]


async def select_rooms(session) -> list[Room]:
    cursor = await session.scalars(select(Room).order_by(Room.id))

    return cursor.all()


async def select_room(session, id: int) -> Room:
    cursor = await session.scalars(select(Room).where(Room.id == id))
    item = cursor.first()
    assert item, OBJECT_NOT_FOUND_ERROR

    return item


async def select_messages_by_room_id(session, room_id: int) -> list[Message]:
    cursor = await session.scalars(
        select(Message).where(Message.room_id == room_id).order_by(Message.id)
    )

    return cursor.all()


async def create_message(
    session,
    room_id: int,
    owner_id: int,
    body: str,
) -> Message:
    new_msg = Message(body=body, owner_id=owner_id, room_id=room_id)
    session.add(new_msg)
    return new_msg


async def delete_message(session, id: int):
    msg = await session.get(Message, id)
    await session.delete(msg)
