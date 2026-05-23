import pytest
from aiohttp import web
from aiohttp_session import (
    SimpleCookieStorage,
    get_session,
    setup as setup_session,
)

from aiohttpdemo_blog.csrf import (
    CSRF_FIELD_NAME,
    CSRF_HEADER_NAME,
    _get_or_create_token,
    csrf_middleware,
)


async def _token_view(request):
    session = await get_session(request)
    token = await _get_or_create_token(session)
    return web.Response(text=token)


async def _protected(request):
    return web.Response(text="ok")


@pytest.fixture
async def csrf_client(aiohttp_client):
    app = web.Application()
    setup_session(app, SimpleCookieStorage())
    app.middlewares.append(csrf_middleware)
    app.router.add_get("/token", _token_view)
    app.router.add_post("/protected", _protected)
    return await aiohttp_client(app)


async def test_safe_method_passes(csrf_client):
    resp = await csrf_client.get("/token")
    assert resp.status == 200


async def test_post_without_token_rejected(csrf_client):
    resp = await csrf_client.post("/protected", data={})
    assert resp.status == 403


async def test_post_with_valid_token_in_form(csrf_client):
    token = await (await csrf_client.get("/token")).text()
    resp = await csrf_client.post(
        "/protected", data={CSRF_FIELD_NAME: token})
    assert resp.status == 200


async def test_post_with_valid_token_in_header(csrf_client):
    token = await (await csrf_client.get("/token")).text()
    resp = await csrf_client.post(
        "/protected", data={}, headers={CSRF_HEADER_NAME: token})
    assert resp.status == 200


async def test_post_with_wrong_token_rejected(csrf_client):
    await csrf_client.get("/token")
    resp = await csrf_client.post(
        "/protected", data={CSRF_FIELD_NAME: "wrong"})
    assert resp.status == 403


async def test_post_without_session_rejected(csrf_client):
    resp = await csrf_client.post(
        "/protected", data={CSRF_FIELD_NAME: "anything"})
    assert resp.status == 403
