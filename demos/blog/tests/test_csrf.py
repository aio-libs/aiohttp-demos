import re

from aiohttpdemo_blog.csrf import CSRF_FIELD_NAME, CSRF_HEADER_NAME

_CSRF_INPUT_RE = re.compile(r'name="_csrf"\s+value="([^"]+)"')


async def _csrf_token(client, path="/login"):
    resp = await client.get(path)
    body = await resp.text()
    match = _CSRF_INPUT_RE.search(body)
    assert match, f"no CSRF token rendered on {path}"
    return match.group(1)


async def test_get_renders_csrf_token(tables_and_data, client):
    resp = await client.get("/login")
    assert resp.status == 200
    assert _CSRF_INPUT_RE.search(await resp.text())


async def test_post_without_token_is_forbidden(tables_and_data, client):
    resp = await client.post(
        "/login", data={"username": "Adam", "password": "adam"})
    assert resp.status == 403


async def test_post_with_form_token_is_accepted(tables_and_data, client):
    token = await _csrf_token(client)
    resp = await client.post(
        "/login",
        data={CSRF_FIELD_NAME: token, "username": "Adam", "password": "adam"},
    )
    assert resp.status != 403


async def test_post_with_header_token_is_accepted(tables_and_data, client):
    token = await _csrf_token(client)
    resp = await client.post(
        "/login",
        data={"username": "Adam", "password": "adam"},
        headers={CSRF_HEADER_NAME: token},
    )
    assert resp.status != 403


async def test_post_with_wrong_token_is_forbidden(tables_and_data, client):
    await _csrf_token(client)  # establish a session with a real token
    resp = await client.post(
        "/login",
        data={CSRF_FIELD_NAME: "wrong", "username": "Adam", "password": "adam"},
    )
    assert resp.status == 403
