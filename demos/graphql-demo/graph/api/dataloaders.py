from typing import Any, List

from aiodataloader import DataLoader
from graph.auth.db_utils import select_users
from graph.auth.models import User
from sqlalchemy.ext.asyncio import async_sessionmaker

__all__ = [
    "UserDataLoader",
]


class BaseAIODataLoader(DataLoader):
    """The base data loader for aiohttp.

    It need create when application initialization with current db engine.
    """

    engine: Any = None

    def __init__(self, engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = engine
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    def sorted_by_keys(self, items: list[User], keys: List[int]) -> list[User]:
        """Help ordering of returned items In `aiodataloader`."""
        items_dict = {key: value for key, value in zip(sorted(set(keys)), items)}

        return [items_dict[key] for key in keys]


class UserDataLoader(BaseAIODataLoader):
    """Simple user data loader.

    Should be used everywhere, when it is possible problem N + 1 requests.
    """

    async def batch_load_fn(self, keys: List[int]) -> list[User]:
        async with self.session.begin() as sess:
            response = await select_users(sess, keys)

        return self.sorted_by_keys(response, keys)
