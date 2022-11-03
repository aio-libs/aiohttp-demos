import asyncio

from .server import init_application
from .settings import PROJECT_ROOT
from .utils import load_config


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import aiohttp_debugtoolbar
    config = load_config(PROJECT_ROOT / "configs" / "base.yml")
    app = await init_application(config)
    aiohttp_debugtoolbar.setup(app)
    return app
