import pytest
from aiohttpdemo_chat.main import init_app


@pytest.fixture
async def client(aiohttp_client):
    app = await init_app()
    return await aiohttp_client(app)
