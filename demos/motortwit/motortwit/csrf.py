import hmac
import re
import secrets

from aiohttp import web


CSRF_FIELD_NAME = "_csrf"
CSRF_COOKIE_NAME = "_csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"

_REQUEST_KEY = "_csrf_token"
_SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})

# secrets.token_urlsafe(32) emits a URL-safe base64 string (43 chars,
# RFC 4648 alphabet without padding). Require both halves of the
# double-submit comparison to fit that shape so anything else is
# rejected before reaching the constant-time compare.
_TOKEN_RE = re.compile(r"\A[A-Za-z0-9_-]{32,128}\Z")


def _tokens_match(cookie_value, submitted_value):
    """Return True only when both inputs look like real CSRF tokens
    and are equal under a constant-time comparison."""
    if not isinstance(cookie_value, str) or not isinstance(submitted_value, str):
        return False
    if not _TOKEN_RE.match(cookie_value):
        return False
    if not _TOKEN_RE.match(submitted_value):
        return False
    return hmac.compare_digest(cookie_value, submitted_value)


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
        if not _tokens_match(cookie_token, submitted):
            raise web.HTTPForbidden(reason="CSRF token missing or invalid")

    response = await handler(request)

    if not cookie_token:
        response.set_cookie(
            CSRF_COOKIE_NAME, token, samesite="Lax", httponly=True)

    return response
