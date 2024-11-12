import random
from unittest.mock import Mock

import pytest
import pytest_asyncio
from graphene.test import Client
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from graph.api.dataloaders import UserDataLoader
from graph.api.views import schema
from graph.auth.models import User
from graph.chat.models import Message, Room
from graph.db import Base
from graph.utils import APP_PATH as PATH
from graph.utils import get_config

# constants
TEST_CONFIG_PATH = PATH / "config" / "api.test.yml"
CONFIG_PATH = PATH / "config" / "api.yml"

config = get_config(["-c", CONFIG_PATH.as_posix()])
test_config = get_config(["-c", TEST_CONFIG_PATH.as_posix()])


# helpers
def get_db_url(config: dict) -> str:
    """Generate a url for db connection from the config."""

    return (
        f"postgresql+asyncpg://"
        f"{config['postgres']['user']}"
        f":{config['postgres']['password']}"
        f"@{config['postgres']['host']}"
        f":{config['postgres']['port']}"
        f"/{config['postgres']['database']}"
    )


engine = create_async_engine(
    get_db_url(config),
    isolation_level="AUTOCOMMIT",
)
test_engine = create_async_engine(
    get_db_url(test_config),
    isolation_level="AUTOCOMMIT",
)


async def setup_test_db(engine) -> None:
    """Creating new test database environment."""
    # test params
    db_name = test_config["postgres"]["database"]
    db_user = test_config["postgres"]["user"]
    db_password = test_config["postgres"]["password"]

    async with engine.connect() as conn:
        await conn.execute(text(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'"))
        await conn.execute(text(f"CREATE DATABASE {db_name} ENCODING 'UTF8'"))
        await conn.execute(text(f"ALTER DATABASE {db_name} OWNER TO {db_user}"))
        await conn.execute(text(f"GRANT ALL ON SCHEMA public TO {db_user}"))


async def teardown_test_db(engine) -> None:
    """Remove the test database environment."""
    # test params
    db_name = test_config["postgres"]["database"]
    db_user = test_config["postgres"]["user"]

    async with engine.connect() as conn:
        await conn.execute(
            text(
                f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
            AND pid <> pg_backend_pid();
            """
            )
        )
        await conn.execute(text(f"drop database if exists {db_name}"))
        await conn.execute(text(f"REVOKE ALL ON SCHEMA public FROM {db_user}"))
        await conn.execute(text(f"drop role if exists {db_user}"))


async def init_sample_data(engine) -> None:
    session = async_sessionmaker(engine, expire_on_commit=False)
    async with session.begin() as sess:
        for idx in range(1000):
            sess.add(
                User(
                    id=idx,
                    username=f"test#{idx}",
                    email=f"test#{idx}",
                    password=f"{idx}",
                )
            )

    rooms_store = []

    async with session.begin() as sess:
        for idx in range(1000):
            new_room = Room(name=f"test#{idx}", owner_id=random.randint(0, 999))
            sess.add(new_room)
            rooms_store.append(new_room)

    async with session.begin() as sess:
        for room in rooms_store:
            for _ in range(10):
                sess.add(
                    Message(
                        body="test",
                        who_like=[
                            random.randint(0, 999) for x in range(random.randint(0, 6))
                        ],
                        owner_id=random.randint(0, 999),
                        room_id=room.id,
                    )
                )


# fixtures
@pytest.fixture
async def db_engine():
    """The fixture provides async engine for PostgresSQl."""
    db = create_async_engine(get_db_url(test_config))
    yield db
    await db.dispose()


@pytest.fixture
async def db_sm(db_engine):
    """The fixture initialize async engine for PostgresSQl."""
    yield async_sessionmaker(db_engine, expire_on_commit=False)


@pytest.fixture
async def requests(db_engine, db_sm):
    """Request for get resource in program from app."""

    class Loaders:
        users = UserDataLoader(db_engine, max_batch_size=100)

    class RedisMock:
        @staticmethod
        async def publish_json(*_):
            return Mock()

    request = Mock()
    request.app = {
        "db": db_sm,
        "redis_pub": RedisMock(),
        "loaders": Loaders(),
    }

    return {"request": request}


@pytest_asyncio.fixture(scope="session")
async def db():
    """The fixture for running and turn down database."""
    await setup_test_db(engine)
    yield
    await teardown_test_db(engine)


@pytest.fixture(scope="session")
async def tables(db):
    """The fixture for create all tables and init simple data."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_sample_data(test_engine)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def client(tables):
    """The fixture for the initialize graphene's client."""
    return Client(schema, return_promise=True)
