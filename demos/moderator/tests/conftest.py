import pytest
from moderator.utils import load_config
from moderator.consts import PROJ_ROOT
from moderator.main import init


@pytest.fixture
def conf():
    return load_config(PROJ_ROOT / 'config' / 'config.yml')


@pytest.fixture
async def api(aiohttp_client, conf):
    app = await init(conf)
    yield await aiohttp_client(app)
    await app.shutdown()
