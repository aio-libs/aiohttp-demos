import asyncio

import pytest
from redis import asyncio as aioredis

from shortify.main import init, PROJ_ROOT
from shortify.utils import load_config

TEST_CONFIG_PATH = PROJ_ROOT / "config" / "config.yml"
TEST_CONFIG = load_config(TEST_CONFIG_PATH.as_posix())


@pytest.fixture
async def cli(aiohttp_client):
    app, _, _ = await init()
    return await aiohttp_client(app)


@pytest.fixture
async def redis():
    """Create a Redis connection for testing."""
    redis_config = TEST_CONFIG["redis"]
    redis = await aioredis.from_url(
        f"redis://{redis_config['host']}:{redis_config['port']}",
    )
    yield redis
    await redis.aclose()
    # Give time for all connections to close properly
    await asyncio.sleep(0.2)


@pytest.fixture(autouse=True)
async def clean_redis(redis):
    """Clean Redis database before each test."""
    await redis.flushdb()
    # Give time for all connections to close properly
    await asyncio.sleep(0.2)
