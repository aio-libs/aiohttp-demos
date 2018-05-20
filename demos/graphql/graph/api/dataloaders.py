from promise import Promise
from aiodataloader import DataLoader

from graph.auth.db_utils import select_users


__all__ = ['UserLoader', ]


class UserLoader(DataLoader):
    engine = None

    def __init__(self, engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = engine

    async def batch_load_fn(self, keys):
        async with self.engine.acquire() as conn:
            response = await select_users(conn, keys)

        return await Promise.resolve(response)
