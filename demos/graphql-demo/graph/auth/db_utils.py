from typing import List

from graph.auth.tables import Users

from sqlalchemy.sql import select


async def select_users(session, keys: List[int]):
    cursor = await session.scalars(select(Users)
                                   .where(Users.id.in_(keys))
                                   .order_by(Users.id))
    return await cursor.all()


async def select_user(session, key: int):
    cursor = await session.scalars(select(Users)
                                   .where(Users.id == key)
                                   .order_by(Users.id))
    return await cursor.first()
