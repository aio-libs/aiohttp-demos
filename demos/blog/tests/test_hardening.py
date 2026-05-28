async def test_login_session_cookie_is_samesite_strict_and_httponly(
    tables_and_data, client
):
    valid_form = {'username': 'Adam', 'password': 'adam'}

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
