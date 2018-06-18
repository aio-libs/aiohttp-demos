import asyncio
import json
from concurrent.futures import ProcessPoolExecutor

import trafaret as t
import yaml

from .consts import PROJ_ROOT
from .exceptions import JsonValidaitonError
from .worker import warm


def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f)
    # TODO: add config validation
    return data


Comment = t.Dict({
    t.Key('comment'): t.String,
})
CommentList = t.List(Comment, max_length=10)


ModerateView = t.Dict({
    t.Key('toxic'): t.Float[0:1],
    t.Key('severe_toxic'): t.Float[0:1],
    t.Key('obscene'): t.Float[0:1],
    t.Key('insult'): t.Float[0:1],
    t.Key('identity_hate'): t.Float[0:1],
})
ModerateList = t.List(ModerateView)


def validate_payload(raw_payload, schema):
    payload = raw_payload.decode(encoding='UTF-8')
    try:
        parsed = json.loads(payload)
    except ValueError:
        raise JsonValidaitonError('Payload is not json serialisable')

    try:
        data = schema(parsed)
    except t.DataError as exc:
        result = exc.as_dict()
        raise JsonValidaitonError(result)
    return data


async def setup_executor(app, conf):
    n = conf['max_workers']

    executor = ProcessPoolExecutor(max_workers=n)
    path = str(PROJ_ROOT / conf['model_path'])
    loop = asyncio.get_event_loop()
    run = loop.run_in_executor
    fs = [run(executor, warm, path) for i in range(0, n)]
    await asyncio.gather(*fs)

    async def close_executor(app):
        # TODO: figureout timeout for shutdown
        executor.shutdown(wait=True)

    app.on_cleanup.append(close_executor)
    app['executor'] = executor
    return executor
