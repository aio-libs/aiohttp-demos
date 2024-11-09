import pytest
from graph.chat.db_utils import (
    create_message,
    delete_message,
    select_messages_by_room_id,
    select_room,
    select_rooms,
)


@pytest.mark.asyncio
async def test_select_room(db_sm):
    async with db_sm() as conn:
        res = await select_room(conn, 1)

    assert res.id == 1


@pytest.mark.asyncio
async def test_select_rooms(db_sm):
    async with db_sm() as conn:
        res = await select_rooms(conn)

    assert isinstance(res, list)
    assert res[0].id == 1


@pytest.mark.asyncio
async def test_select_messages_by_room_id(db_sm):
    async with db_sm() as conn:
        res = await select_messages_by_room_id(conn, 1)

    assert isinstance(res, list)


@pytest.mark.asyncio
async def test_create_message(db_sm):
    async with db_sm() as conn:
        await create_message(conn, 1, 1, "Text")


@pytest.mark.asyncio
async def test_delete_message(db_sm):
    async with db_sm() as conn:
        await delete_message(conn, 1)
