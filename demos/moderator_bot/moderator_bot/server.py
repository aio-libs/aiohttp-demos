import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

from aiohttp import web
from aioslacker import Slacker

from .giphy import GiphyClient
from .handlers import MainHandler
from .router import setup_main_handler
from .settings import GIPHY_API_KEY, MAX_WORKERS, PROJECT_ROOT, SLACK_BOT_TOKEN
from .utils import load_config
from .worker import warm


def setup_cleanup_hooks(tasks):
    async def cleanup(app):
        for func in tasks:
            result = func()
            if asyncio.iscoroutine(result):
                result = await result

    return cleanup


def setup_startup_hooks(loop, executor, model_path, workers_count):
    async def startup(app):
        run = partial(loop.run_in_executor, executor, warm, model_path)
        coros = [run() for _ in range(0, workers_count)]
        await asyncio.gather(*coros)

    return startup


async def init_application(loop, config):
    app = web.Application(debug=config["debug"])

    executor = ProcessPoolExecutor(MAX_WORKERS)

    slack_client = Slacker(SLACK_BOT_TOKEN)
    giphy_client = GiphyClient(loop, GIPHY_API_KEY, config["request_timeout"])

    handler = MainHandler(
        loop,
        executor,
        slack_client,
        giphy_client,
    )

    model_path = Path(config["model_path"])

    setup_main_handler(app, handler)

    app.on_startup.append(setup_startup_hooks(
        loop,
        executor,
        model_path,
        MAX_WORKERS,
    ))

    app.on_cleanup.append(setup_cleanup_hooks([
        partial(executor.shutdown, wait=True),
        slack_client.close,
        giphy_client.close,
    ]))

    return app


def main():
    loop = asyncio.get_event_loop()
    config = load_config(PROJECT_ROOT / "configs" / "base.yml")
    app = init_application(loop, config)
    web.run_app(app, host=config["host"], port=config["port"])
