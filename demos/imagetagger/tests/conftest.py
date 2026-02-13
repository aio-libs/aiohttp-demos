import pytest

from imagetagger.utils import config_from_dict
from imagetagger.app import init_app


@pytest.fixture(scope='session')
def conf():
    d = {
        'app': {'host': 'localhost', 'port': 9100},
        'workers': {'max_workers': 1,
                    'model_path': 'tests/data/mobilenet.h5'},
    }
    return config_from_dict(d)


@pytest.fixture
async def api(aiohttp_client, conf):
    app = await init_app(conf)
    yield await aiohttp_client(app)
    await app.shutdown()
