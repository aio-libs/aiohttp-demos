import pathlib

import pytest

from aiohttpdemo_polls.main import init
from aiohttpdemo_polls.config import DB_CONFIG_USER
from .init_db import setup_db, create_tables, sample_data, teardown_db


BASE_DIR = pathlib.Path(__file__).parent.parent


@pytest.fixture
def config_path():
    path = BASE_DIR / 'config' / 'polls.yaml'
    return path.as_posix()


@pytest.fixture
def cli(loop, test_client, config_path, app_db):
    print('in cli fixture')
    app = init(loop, ['-c', config_path])
    return loop.run_until_complete(test_client(app))


@pytest.fixture
def app_db():

    print('in app_db fixture')

    db_name = DB_CONFIG_USER['database']
    db_user = DB_CONFIG_USER['user']
    db_pass = DB_CONFIG_USER['password']

    setup_db(db_name, db_user, db_pass)
    create_tables()
    sample_data()

    print('before app_db yield')

    yield

    print('after app_db yield')
    teardown_db(db_name, db_user)
