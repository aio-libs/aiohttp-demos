import pytest

from graph.auth.db_utils import select_user, select_users


@pytest.mark.asyncio
async def test_select_user(sa_engine):
    async with sa_engine.acquire() as conn:
        res = await select_user(conn, 1)

    assert res.id == 1


@pytest.mark.asyncio
async def test_select_users(sa_engine):
    async with sa_engine.acquire() as conn:
        res = await select_users(conn, [1, 2, 3])

    assert isinstance(res, list)
    assert res[0].id == 1
