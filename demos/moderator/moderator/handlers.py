import asyncio
import numpy as np
from aiohttp import web

from .worker import predict_proba
from .utils import CommentList, ModerateList, validate_payload


class SiteHandler:

    def __init__(self, conf, executor, project_root):
        self._conf = conf
        self._executor = executor
        self._root = project_root
        self._loop = asyncio.get_event_loop()

    async def index(self, request):
        path = str(self._root / 'static' / 'index.html')
        return web.FileResponse(path)

    async def moderate(self, request):
        raw_data = await request.read()
        data = validate_payload(raw_data, CommentList)

        features = np.array([d['comment'] for d in data])
        r = self._loop.run_in_executor
        results = await r(self._executor, predict_proba, features)
        results = np.array(results).T[1].tolist()

        payload = ModerateList([{
            'toxic': f'{r[0]:.2f}',
            'severe_toxic': f'{r[1]:.2f}',
            'obscene': f'{r[2]:.2f}',
            'insult': f'{r[3]:.2f}',
            'identity_hate': f'{r[4]:.2f}'
        } for r in results])
        return web.json_response(payload)
