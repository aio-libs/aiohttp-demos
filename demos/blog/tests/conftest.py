import pytest

from aiohttpdemo_blog.main import init_app
from aiohttpdemo_blog.settings import load_config, BASE_DIR
from db_helpers import (
    setup_db, teardown_db,
    create_tables, create_sample_data, drop_tables
)


@pytest.fixture
async def client(aiohttp_client):
    config = load_config(BASE_DIR / 'config' / 'test_config.toml')
    app = await init_app(config)
    return await aiohttp_client(app)


@pytest.fixture
async def gino_db(client):
    return client.app['db']


@pytest.fixture(scope='session')
def database():
    admin_db_config = load_config(BASE_DIR / 'config' / 'admin_config.toml')['database']
    test_db_config = load_config(BASE_DIR / 'config' / 'test_config.toml')['database']

    setup_db(executor_config=admin_db_config, target_config=test_db_config)
    yield
    teardown_db(executor_config=admin_db_config, target_config=test_db_config)


@pytest.fixture
async def tables_and_data(database, gino_db):
    await create_tables(gino_db)
    await create_sample_data()

    yield

    await drop_tables(gino_db)
