from unittest.mock import Mock

import aiopg.sa
import pytest
import random
from sqlalchemy import create_engine

from graph.api.dataloaders import UserDataLoader
from graph.api.views import schema
from graph.auth.tables import users
from graph.chat.tables import (
    rooms,
    messages,
)
from graph.db import metadata
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
    '''
    Generate a url for db connection from the config.
    '''

    return (
        f"postgresql://"
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
test_engine = create_engine(
    get_db_url(test_config),
    isolation_level='AUTOCOMMIT',
)


def setup_test_db(engine) -> None:
    '''
    Removing the old test database environment and creating new clean
    environment.
    '''
    # test params
    db_name = test_config['postgres']['database']
    db_user = test_config['postgres']['user']
    db_password = test_config['postgres']['password']

    teardown_test_db(engine)

    with engine.connect() as conn:
        conn.execute(
            f"create user {db_user} with password '{db_password}'"
        )
        conn.execute(
            f"create database {db_name} encoding 'UTF8'"
        )
        conn.execute(
            f"grant all privileges on database {db_name} to {db_user}"
        )


def teardown_test_db(engine) -> None:
    '''
    Removing the test database environment.
    '''
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
        conn.execute(f"drop role if exists {db_user}")


def init_sample_data(engine) -> None:
    with engine.connect() as conn:
        query = users\
            .insert()\
            .values([{
                    'id': idx,
                    'username': f'test#{idx}',
                    'email': f'test#{idx}',
                    'password': f'{idx}'} for idx in range(1000)
                ])\
            .returning(users.c.id)

        response = conn.execute(query)
        users_idx = [user[0] for user in response]

        query = rooms\
            .insert()\
            .values([{
                'name': f'test#{idx}',
                'owner_id': random.choice(users_idx)} for idx in users_idx
            ])\
            .returning(rooms.c.id)

        response = conn.execute(query)
        rooms_idx = [room[0] for room in response]
        values = []

        for room in rooms_idx:
            for i in range(10):
                values.append({
                    'body': "test",
                    'who_like': random.sample(users_idx, random.randint(0, 5)),
                    'owner_id': random.choice(users_idx),
                    'room_id': room,
                })

        conn.execute(messages.insert().values(values))


# fixtures
@pytest.fixture
async def sa_engine(loop):
    '''
    The fixture initialize async engine for PostgresSQl.
    '''

    return await aiopg.sa.create_engine(**test_config['postgres'])


@pytest.fixture
async def requests(sa_engine):
    '''
    In the graphene's client u should put request for get resource in program
    from app.
    '''
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


@pytest.yield_fixture(scope='session')
def db():
    '''
    The fixture for running and turn down database.
    '''
    setup_test_db(engine)
    yield
    teardown_test_db(engine)


@pytest.yield_fixture(scope='session')
def tables(db):
    '''
    The fixture for create all tables and init simple data.
    '''
    metadata.create_all(test_engine)
    init_sample_data(test_engine)
    yield
    metadata.drop_all(test_engine)


@pytest.fixture(scope='session')
def client(tables):
    '''
    The fixture for the initialize graphene's client.
    '''
    return Client(schema, return_promise=True)
