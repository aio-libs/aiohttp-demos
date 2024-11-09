from typing import List

from graph.auth.models import User

from sqlalchemy.sql import select


async def select_users(session, keys: List[int]):
    result = await session.scalars(
        select(User).where(User.id.in_(keys)).order_by(User.id)
    )
    return result.all()


async def select_user(session, key: int):
    result = await session.scalars(select(User).where(User.id == key).order_by(User.id))
    return result.first()
