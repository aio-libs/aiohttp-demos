import pytest
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from aiohttpdemo_polls.main import init_app
from aiohttpdemo_polls.settings import BASE_DIR, get_config
from init_db import (
    setup_db,
    teardown_db,
    create_tables,
    sample_data,
    drop_tables
)

DSN = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
TEST_CONFIG_PATH = BASE_DIR / 'config' / 'polls_test.yaml'
TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
TEST_DB_URL = DSN.format(**TEST_CONFIG['postgres'])


@pytest.fixture
async def cli(aiohttp_client, db):
    app = await init_app(['-c', TEST_CONFIG_PATH.as_posix()])
    return await aiohttp_client(app)


@pytest.fixture(scope='module')
async def db():
    test_config = get_config(['-c', TEST_CONFIG_PATH.as_posix()])

    await setup_db(test_config['postgres'])
    yield
    await teardown_db(test_config['postgres'])

@pytest.fixture(scope="module")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def tables_and_data():
    test_engine = create_async_engine(TEST_DB_URL)
    await create_tables(test_engine)
    await sample_data(test_engine)
    yield
    await drop_tables(test_engine)
