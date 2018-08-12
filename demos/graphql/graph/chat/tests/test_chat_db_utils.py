import pytest

from graph.chat.db_utils import (
    select_room,
    select_rooms,
    select_messages_by_room_id,
    create_message,
    delete_message,
)


@pytest.mark.asyncio
async def test_select_room(sa_engine):
    async with sa_engine.acquire() as conn:
        res = await select_room(conn, 1)

    assert res.id == 1


@pytest.mark.asyncio
async def test_select_rooms(sa_engine):
    async with sa_engine.acquire() as conn:
        res = await select_rooms(conn)

    assert isinstance(res, list)
    assert res[0].id == 1


@pytest.mark.asyncio
async def test_select_messages_by_room_id(sa_engine):
    async with sa_engine.acquire() as conn:
        res = await select_messages_by_room_id(conn, 1)

    assert isinstance(res, list)


@pytest.mark.asyncio
async def test_create_message(sa_engine):
    async with sa_engine.acquire() as conn:
        await create_message(conn, 1, 1, 'Text')


@pytest.mark.asyncio
async def test_delete_message(sa_engine):
    async with sa_engine.acquire() as conn:
        await delete_message(conn, 1)
