import pytest

from imagetagger.utils import config_from_dict
from imagetagger.app import init_app


@pytest.fixture
def loop(event_loop):
    return event_loop


@pytest.fixture(scope='session')
def conf():
    d = {
        'app': {'host': 'localhost', 'port': 9100},
        'workers': {'max_workers': 1,
                    'model_path': 'tests/data/mobilenet.h5'},
    }
    return config_from_dict(d)


@pytest.fixture
def api(loop, aiohttp_client, conf):
    app = loop.run_until_complete(init_app(conf))
    yield loop.run_until_complete(aiohttp_client(app))
    loop.run_until_complete(app.shutdown())
