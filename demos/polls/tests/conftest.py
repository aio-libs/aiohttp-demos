import pathlib

import pytest

from aiohttpdemo_polls.main import init
from aiohttpdemo_polls.config import DB_CONFIG_USER
from .init_db import (
    setup_db,
    teardown_db,
    create_tables, 
    sample_data,
    drop_tables
)


BASE_DIR = pathlib.Path(__file__).parent.parent


@pytest.fixture
def config_path():
    path = BASE_DIR / 'config' / 'polls.yaml'
    return path.as_posix()


@pytest.fixture
def cli(loop, test_client, config_path, db):
    app = init(loop, ['-c', config_path])
    return loop.run_until_complete(test_client(app))


@pytest.fixture(scope='module')
def db():
    db_name = DB_CONFIG_USER['database']
    db_user = DB_CONFIG_USER['user']
    db_pass = DB_CONFIG_USER['password']

    setup_db(db_name, db_user, db_pass)
    yield
    teardown_db(db_name, db_user)


@pytest.fixture
def tables_and_data():
    create_tables()
    sample_data()
    yield
    drop_tables()
