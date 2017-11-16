import pathlib

import pytest

from aiohttpdemo_polls.main import init
from .init_db import (
    get_config,
    setup_db,
    teardown_db,
    create_tables,
    sample_data,
    drop_tables
)


BASE_DIR = pathlib.Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / 'config' / 'polls_test.yaml'


@pytest.fixture
def cli(loop, test_client, db):
    app = init(['-c', CONFIG_PATH.as_posix()])
    return loop.run_until_complete(test_client(app))


@pytest.fixture(scope='module')
def db():
    test_config = get_config(CONFIG_PATH)

    setup_db(test_config)
    yield
    teardown_db(test_config)


@pytest.fixture
def tables_and_data():
    create_tables()
    sample_data()
    yield
    drop_tables()
