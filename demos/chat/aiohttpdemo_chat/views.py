import logging

import aiohttp
import aiohttp_jinja2
from aiohttp import web
from faker import Faker

log = logging.getLogger(__name__)

ws_key = web.AppKey("ws_key", dict[str, web.WebSocketResponse])


def get_random_name():
    fake = Faker()
    return fake.name()


async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})

    await ws_current.prepare(request)

    name = get_random_name()
    log.info('%s joined.', name)

    await ws_current.send_json({'action': 'connect', 'name': name})

    for ws in request.app[ws_key].values():
        await ws.send_json({'action': 'join', 'name': name})
    request.app[ws_key][name] = ws_current

    while True:
        msg = await ws_current.receive()

        if msg.type == aiohttp.WSMsgType.text:
            for ws in request.app[ws_key].values():
                if ws is not ws_current:
                    await ws.send_json(
                        {'action': 'sent', 'name': name, 'text': msg.data})
        else:
            break

    del request.app[ws_key][name]
    log.info('%s disconnected.', name)
    for ws in request.app[ws_key].values():
        await ws.send_json({'action': 'disconnect', 'name': name})

    return ws_current
