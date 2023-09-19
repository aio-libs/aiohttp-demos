from unittest.mock import Mock

import pytest
import random

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from graph.api.dataloaders import UserDataLoader
from graph.api.views import schema
from graph.auth.models import User
from graph.chat.models import Room, Message
from graph.db import Base
from graph.utils import (
    APP_PATH as PATH,
    get_config,
)
from graphene.test import Client

# constants
TEST_CONFIG_PATH = PATH / 'config' / 'api.test.yml'
CONFIG_PATH = PATH / 'config' / 'api.yml'

config = get_config(['-c', CONFIG_PATH.as_posix()])
test_config = get_config(['-c', TEST_CONFIG_PATH.as_posix()])


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


engine = create_engine(
    get_db_url(config),
    isolation_level='AUTOCOMMIT',
)
test_engine = create_async_engine(
    get_db_url(test_config),
    isolation_level='AUTOCOMMIT',
)


def setup_test_db(engine) -> None:
    """Creating new test database environment."""
    # test params
    db_name = test_config['postgres']['database']
    db_user = test_config['postgres']['user']
    db_password = test_config['postgres']['password']

    with engine.connect() as conn:
        conn.execute(
            f"create user {db_user} with password '{db_password}'"
        )
        conn.execute(
            f"create database {db_name} encoding 'UTF8'"
        )
        conn.execute(f"alter database {db_name} owner to {db_user}")
        conn.execute(f"grant all on schema public to {db_user}")


def teardown_test_db(engine) -> None:
    """Remove the test database environment."""
    # test params
    db_name = test_config['postgres']['database']
    db_user = test_config['postgres']['user']

    with engine.connect() as conn:
        conn.execute(
            f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
            AND pid <> pg_backend_pid();
            """
        )
        conn.execute(f"drop database if exists {db_name}")
        conn.execute(f"REVOKE ALL ON SCHEMA public FROM {db_user}")
        conn.execute(f"drop role if exists {db_user}")


async def init_sample_data(engine) -> None:
    session = async_sessionmaker(engine, expire_on_commit=False)
    async with session.begin() as sess:
        for idx in range(1000):
            sess.add(User(
                id=idx,
                username=f"test#{idx}",
                email=f"test#{idx}",
                password=f"{idx}"
            ))

    async with session.begin() as sess:
        for idx in range(1000):
            sess.add(Room(name=f"test#{idx}", owner_id=random.randint(0, 999)))

    async with session.begin() as sess:
        for idx in range(1000):
            for _ in range(10):
                sess.add(Message(
                    body="test",
                    who_like=[random.randint(0, 999) for x in range(random.randint(0, 6))],
                    owner_id=random.randint(0, 999),
                    room_id=idx
                ))


# fixtures
@pytest.fixture
async def sa_engine(event_loop):
    """The fixture initialize async engine for PostgresSQl."""
    db = create_async_engine(get_db_url(test_config))
    yield async_sessionmaker(db, expire_on_commit=False)
    await db.dispose()


@pytest.fixture
async def requests(sa_engine):
    """Request for get resource in program from app."""
    class Loaders:
        users = UserDataLoader(sa_engine, max_batch_size=100)

    class RedisMock:
        @staticmethod
        async def publish_json(*_):
            return Mock()

    request = Mock()
    request.app = {
        'db': sa_engine,
        'redis_pub': RedisMock(),
        'loaders': Loaders(),
    }

    return {'request': request}


@pytest.fixture(scope="session")
def db():
    """The fixture for running and turn down database."""
    setup_test_db(engine)
    yield
    teardown_test_db(engine)


@pytest.fixture(scope="session")
async def tables(db):
    """The fixture for create all tables and init simple data."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_sample_data(test_engine)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def client(tables):
    """The fixture for the initialize graphene's client."""
    return Client(schema, return_promise=True)
