import secrets

from aiohttp import web
from aiohttp_session import get_session


CSRF_FIELD_NAME = "_csrf"
CSRF_SESSION_KEY = "_csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"

_SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


async def _get_or_create_token(session):
    token = session.get(CSRF_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
    return token


async def csrf_ctx_processor(request):
    session = await get_session(request)
    return {"csrf_token": await _get_or_create_token(session)}


@web.middleware
async def csrf_middleware(request, handler):
    if request.method in _SAFE_METHODS:
        return await handler(request)

    session = await get_session(request)
    expected = session.get(CSRF_SESSION_KEY)

    submitted = request.headers.get(CSRF_HEADER_NAME)
    if submitted is None:
        form = await request.post()
        submitted = form.get(CSRF_FIELD_NAME)

    if (not expected
            or not submitted
            or not secrets.compare_digest(str(expected), str(submitted))):
        raise web.HTTPForbidden(reason="CSRF token missing or invalid")

    return await handler(request)
