import secrets

from aiohttp import web


CSRF_FIELD_NAME = "_csrf"
CSRF_COOKIE_NAME = "_csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"

_REQUEST_KEY = "_csrf_token"
_SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


async def csrf_ctx_processor(request):
    return {"csrf_token": request.get(_REQUEST_KEY, "")}


@web.middleware
async def csrf_middleware(request, handler):
    cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
    token = cookie_token or secrets.token_urlsafe(32)
    request[_REQUEST_KEY] = token

    if request.method not in _SAFE_METHODS:
        submitted = request.headers.get(CSRF_HEADER_NAME)
        if submitted is None:
            form = await request.post()
            submitted = form.get(CSRF_FIELD_NAME)
        # The double-submit pattern intentionally compares two
        # user-controlled values; the security comes from the
        # same-origin policy preventing the attacker from ever
        # reading the victim's cookie.
        if (not cookie_token
                or not submitted
                or not secrets.compare_digest(  # nosec
                    cookie_token, str(submitted))):
            raise web.HTTPForbidden(reason="CSRF token missing or invalid")

    response = await handler(request)

    if not cookie_token:
        response.set_cookie(
            CSRF_COOKIE_NAME, token, samesite="Lax", httponly=True)

    return response
