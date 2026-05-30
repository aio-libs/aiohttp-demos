import re

import pytest
from aiohttp import web
from aiohttp_security import CookiesIdentityPolicy
from aiohttp_security import setup as setup_security

from motortwit.csrf import (
    CSRF_COOKIE_NAME,
    CSRF_FIELD_NAME,
    CSRF_HEADER_NAME,
    csrf_middleware,
)
from motortwit.main import PROJ_ROOT, setup_jinja
from motortwit.routes import setup_routes
from motortwit.security import AuthorizationPolicy
from motortwit.views import SiteHandler

_CSRF_INPUT_RE = re.compile(r'name="_csrf"\s+value="([^"]+)"')


@pytest.fixture
async def client(aiohttp_client):
    # Build the app from the demo's real wiring (middleware, jinja context
    # processor, templates, routes, handler) so the test exercises the
    # actual CSRF integration. Mongo is unused by /login (GET) and /logout
    # (POST), the two CSRF-relevant endpoints that don't hit the database,
    # so it is left as None (CI has no MongoDB).
    app = web.Application(middlewares=[csrf_middleware])
    setup_jinja(app)
    setup_security(app, CookiesIdentityPolicy(), AuthorizationPolicy(None))
    setup_routes(app, SiteHandler(None), PROJ_ROOT)
    return await aiohttp_client(app)


def _cookie_token(client):
    cookies = client.session.cookie_jar.filter_cookies(client.make_url("/"))
    return cookies[CSRF_COOKIE_NAME].value


async def test_get_login_sets_cookie_and_renders_matching_token(client):
    resp = await client.get("/login")
    assert resp.status == 200
    match = _CSRF_INPUT_RE.search(await resp.text())
    assert match, "login page did not render a CSRF token"
    # double-submit: the rendered token must equal the cookie token
    assert match.group(1) == _cookie_token(client)


async def test_post_without_token_is_forbidden(client):
    resp = await client.post("/logout", data={})
    assert resp.status == 403


async def test_post_with_cookie_but_no_token_is_forbidden(client):
    await client.get("/login")  # establishes the CSRF cookie
    resp = await client.post("/logout", data={})
    assert resp.status == 403


async def test_post_with_form_token_is_accepted(client):
    token = _CSRF_INPUT_RE.search(
        await (await client.get("/login")).text()).group(1)
    resp = await client.post(
        "/logout", data={CSRF_FIELD_NAME: token}, allow_redirects=False)
    assert resp.status == 302


async def test_post_with_header_token_is_accepted(client):
    token = _CSRF_INPUT_RE.search(
        await (await client.get("/login")).text()).group(1)
    resp = await client.post(
        "/logout", data={}, headers={CSRF_HEADER_NAME: token},
        allow_redirects=False)
    assert resp.status == 302


async def test_post_with_wrong_token_is_forbidden(client):
    await client.get("/login")  # establishes a real cookie token
    resp = await client.post(
        "/logout", data={CSRF_FIELD_NAME: "wrong"})
    assert resp.status == 403
