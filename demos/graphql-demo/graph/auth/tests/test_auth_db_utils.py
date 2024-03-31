import pytest

from sqlalchemy.ext.asyncio import async_sessionmaker
from graph.auth.db_utils import select_user, select_users


@pytest.mark.asyncio
async def test_select_user(sa_engine):
    session = async_sessionmaker(sa_engine)

    async with session.begin() as sess:
        res = await select_user(sess, 1)

    assert res.id == 1


@pytest.mark.asyncio
async def test_select_users(sa_engine):
    session = async_sessionmaker(sa_engine)
    
    async with session.begin() as sess:
        res = await select_users(sess, [1, 2, 3])

    assert isinstance(res, list)
    assert res[0].id == 1
