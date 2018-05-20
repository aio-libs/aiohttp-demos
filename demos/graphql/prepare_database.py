import asyncio

import aiopg.sa
from aiopg.sa import SAConnection
import psycopg2
from sqlalchemy.dialects.postgresql import (
    CreateEnumType,
    DropEnumType,
)
from sqlalchemy.schema import (
    CreateTable,
    DropTable,
)

from graph.utils import get_config
from graph.auth.tables import (
    users,
    gender_enum,
)
from graph.chat.tables import (
    rooms,
    messages,
)


tables = [users, rooms, messages, ]
enums = [gender_enum, ]


async def drop_tables(conn: SAConnection) -> None:
    for table in reversed(tables):
        try:
            await conn.execute(DropTable(table))
        except psycopg2.ProgrammingError:
            pass

    for enum in enums:
        try:
            await conn.execute(DropEnumType(enum))
        except psycopg2.ProgrammingError:
            pass


async def create_tables(conn: SAConnection) -> None:
    for enum in enums:
        await conn.execute(CreateEnumType(enum))

    for table in tables:
        await conn.execute(CreateTable(table))


async def create_engine():
    config = get_config()
    config = config['postgres']
    engine = await aiopg.sa.create_engine(**config)

    return engine


async def main():
    print("Start to generate new data..")
    engine = await create_engine()

    try:
        async with engine.acquire() as conn:
            await drop_tables(conn)
            await create_tables(conn)
    finally:
        engine.close()

    print("Finished!")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
