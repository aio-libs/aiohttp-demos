import pytest
import asyncio
from shortify.main import init, PROJ_ROOT
from shortify.utils import load_config
from redis import asyncio as aioredis

TEST_CONFIG_PATH = PROJ_ROOT / "config" / "shortify_test.yaml"
TEST_CONFIG = load_config(TEST_CONFIG_PATH.as_posix())


@pytest.fixture
async def cli(aiohttp_client):
    app, _, _ = await init()
    client = await aiohttp_client(app)
    return client

@pytest.fixture
async def redis():
    """Create a Redis connection for testing."""
    redis_config = TEST_CONFIG["redis"]
    redis = await aioredis.from_url(
        f"redis://{redis_config['host']}:{redis_config['port']}",
    )
    yield redis
    await redis.aclose()


@pytest.fixture
async def clean_redis(redis):
    """Clean Redis database before each test."""
    await redis.flushdb()
    yield
    await redis.flushdb()
