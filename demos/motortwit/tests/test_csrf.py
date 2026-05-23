import pytest
from aiohttp import web

from motortwit.csrf import (
    CSRF_COOKIE_NAME,
    CSRF_FIELD_NAME,
    CSRF_HEADER_NAME,
    csrf_middleware,
)


async def _index(request):
    return web.Response(text="ok")


async def _protected(request):
    return web.Response(text="ok")


@pytest.fixture
async def csrf_client(aiohttp_client):
    app = web.Application(middlewares=[csrf_middleware])
    app.router.add_get("/", _index)
    app.router.add_post("/protected", _protected)
    return await aiohttp_client(app)


async def test_get_sets_csrf_cookie(csrf_client):
    resp = await csrf_client.get("/")
    assert resp.status == 200
    assert CSRF_COOKIE_NAME in resp.cookies


async def test_post_without_cookie_or_token_rejected(csrf_client):
    resp = await csrf_client.post("/protected", data={})
    assert resp.status == 403


async def test_post_with_cookie_only_rejected(csrf_client):
    await csrf_client.get("/")
    resp = await csrf_client.post("/protected", data={})
    assert resp.status == 403


async def test_post_with_form_token_matching_cookie_succeeds(csrf_client):
    await csrf_client.get("/")
    token = csrf_client.session.cookie_jar.filter_cookies(
        csrf_client.make_url("/"))[CSRF_COOKIE_NAME].value
    resp = await csrf_client.post(
        "/protected", data={CSRF_FIELD_NAME: token})
    assert resp.status == 200


async def test_post_with_header_token_matching_cookie_succeeds(csrf_client):
    await csrf_client.get("/")
    token = csrf_client.session.cookie_jar.filter_cookies(
        csrf_client.make_url("/"))[CSRF_COOKIE_NAME].value
    resp = await csrf_client.post(
        "/protected", data={}, headers={CSRF_HEADER_NAME: token})
    assert resp.status == 200


async def test_post_with_wrong_token_rejected(csrf_client):
    await csrf_client.get("/")
    resp = await csrf_client.post(
        "/protected", data={CSRF_FIELD_NAME: "wrong"})
    assert resp.status == 403


async def test_get_reuses_existing_cookie(csrf_client):
    resp1 = await csrf_client.get("/")
    resp2 = await csrf_client.get("/")
    # second response should not Set-Cookie again (cookie already present)
    assert CSRF_COOKIE_NAME in resp1.cookies
    assert CSRF_COOKIE_NAME not in resp2.cookies
