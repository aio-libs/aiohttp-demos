import pytest
from aiohttp import web
from aiohttp_security import CookiesIdentityPolicy
from aiohttp_security import setup as setup_security

from motortwit.main import PROJ_ROOT, setup_jinja
from motortwit.routes import setup_routes
from motortwit.security import AuthorizationPolicy
from motortwit.views import SiteHandler

# The identity is stored in this cookie by CookiesIdentityPolicy.
_IDENTITY_COOKIE = CookiesIdentityPolicy()._cookie_name


@pytest.fixture
async def client(aiohttp_client):
    # Build the app from the demo's real wiring so the guard is exercised
    # through the real security middleware. /register only queries Mongo for
    # a *valid* identity, so the malformed-identity case under test never
    # touches the database (CI has no MongoDB).
    app = web.Application()
    setup_jinja(app)
    setup_security(app, CookiesIdentityPolicy(), AuthorizationPolicy(None))
    setup_routes(app, SiteHandler(None), PROJ_ROOT)
    return await aiohttp_client(app)


@pytest.mark.parametrize("identity", [
    "not-an-objectid",
    "short",
    "x" * 24,        # right length, wrong alphabet
    "deadbeef",
])
async def test_malformed_identity_cookie_is_treated_as_unauthenticated(
        client, identity):
    # Without the AuthorizationPolicy guard, ObjectId(identity) raises
    # InvalidId and the request 500s. The guard makes the real app treat a
    # malformed cookie as anonymous and render the page normally.
    resp = await client.get(
        "/register", cookies={_IDENTITY_COOKIE: identity})
    assert resp.status == 200
