import pytest
from moderator_bot.server import init_application
from moderator_bot.settings import PROJECT_ROOT
from moderator_bot.utils import load_config


@pytest.fixture
def config():
    return load_config(PROJECT_ROOT / "configs" / "base.yml")


@pytest.fixture
async def client(aiohttp_client, loop, config):
    app = await init_application(loop, config)
    return await aiohttp_client(app)
