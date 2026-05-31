import re

_CSRF_INPUT_RE = re.compile(r'name="_csrf"\s+value="([^"]+)"')


async def test_login_session_cookie_is_samesite_strict_and_httponly(
    tables_and_data, client
):
    # GET first to obtain the CSRF token (and session cookie); POST /login
    # is CSRF-protected, so a tokenless POST would be rejected with 403.
    token_page = await client.get("/login")
    token = _CSRF_INPUT_RE.search(await token_page.text()).group(1)
    valid_form = {'_csrf': token, 'username': 'Adam', 'password': 'adam'}

    async with client.post(
        "/login", data=valid_form, allow_redirects=False
    ) as resp:
        assert resp.status == 302
        cookie_headers = resp.headers.getall("Set-Cookie")

    session_cookie = next(
        h for h in cookie_headers if h.startswith("AIOHTTP_SESSION=")
    )
    assert "httponly" in session_cookie.lower()
    assert "samesite=strict" in session_cookie.lower()
