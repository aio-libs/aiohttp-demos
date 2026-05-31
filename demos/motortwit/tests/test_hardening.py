import asyncio

import pytest
from aiohttp import web
from aiohttp_security import CookiesIdentityPolicy
from aiohttp_security import setup as setup_security

from motortwit.main import PROJ_ROOT, init, setup_jinja
from motortwit.routes import setup_routes
from motortwit.security import AuthorizationPolicy, generate_password_hash
from motortwit.views import SiteHandler

# The identity is stored in this cookie by CookiesIdentityPolicy.
_IDENTITY_COOKIE = CookiesIdentityPolicy()._cookie_name


@pytest.fixture
async def client(aiohttp_client):
    # Boot the real app via main.init(). The malformed-identity case under
    # test never reaches a Mongo query (the AuthorizationPolicy guard
    # short-circuits), so the lazily created Mongo client is never contacted
    # (CI has no MongoDB).
    app, _, _ = await init(asyncio.get_running_loop())
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


class _FakeUsers:
    """Stand-in for the Mongo `user` collection used by the login flow."""

    def __init__(self, user):
        self._user = user

    async def find_one(self, _query):
        return self._user


class _FakeMongo:
    def __init__(self, user):
        self.user = _FakeUsers(user)


async def _client_with_user(aiohttp_client, user):
    # Same wiring as main.init(), but with a fake Mongo whose user lookup
    # returns `user`, so /login can run without a real database (CI has none).
    mongo = _FakeMongo(user)
    app = web.Application()
    setup_jinja(app)
    setup_security(app, CookiesIdentityPolicy(), AuthorizationPolicy(mongo))
    setup_routes(app, SiteHandler(mongo), PROJ_ROOT)
    return await aiohttp_client(app)


async def test_login_sets_strict_httponly_identity_cookie(aiohttp_client):
    # A successful login must pin the identity cookie to SameSite=Strict and
    # HttpOnly so it is never sent on cross-site requests nor read from JS.
    user = {"_id": "a" * 24, "username": "bob",
            "pw_hash": generate_password_hash("s3cret")}
    client = await _client_with_user(aiohttp_client, user)

    resp = await client.post(
        "/login", data={"username": "bob", "password": "s3cret"},
        allow_redirects=False)

    assert resp.status == 302  # redirect to the timeline on success
    set_cookie = "; ".join(resp.headers.getall("Set-Cookie"))
    assert "SameSite=Strict" in set_cookie
    assert "HttpOnly" in set_cookie


async def test_login_page_escapes_reflected_username(aiohttp_client):
    # The login template reflects the submitted username into a value=""
    # attribute. Autoescaping (the aiohttp-jinja2 default we now rely on after
    # dropping the explicit select_autoescape) must escape the markup so it
    # cannot break out of the attribute and inject script.
    client = await _client_with_user(aiohttp_client, None)  # unknown user
    payload = '"><script>alert(1)</script>'

    resp = await client.post(
        "/login", data={"username": payload, "password": "x"})

    assert resp.status == 200  # invalid username re-renders the login page
    body = await resp.text()
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in body
