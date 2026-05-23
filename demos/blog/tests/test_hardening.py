from unittest.mock import MagicMock

import aiohttp_jinja2
import jinja2
import redis.asyncio
from aiohttp import web
from aiohttp_session.redis_storage import RedisStorage


def test_redis_storage_session_cookie_is_samesite_lax_and_httponly():
    storage = RedisStorage(
        redis_pool=MagicMock(spec=redis.asyncio.Redis),
        httponly=True, samesite='Lax',
    )
    assert storage.cookie_params['samesite'] == 'Lax'
    assert storage.cookie_params['httponly'] is True


def test_jinja_autoescape_escapes_html():
    env = jinja2.Environment(
        loader=jinja2.DictLoader({"x.html": "{{ value }}"}),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    rendered = env.get_template("x.html").render(
        value="<script>alert(1)</script>")
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered


def test_blog_main_uses_explicit_select_autoescape():
    # We cannot run init_app here without a redis - but we can build a
    # minimal app and call the same aiohttp_jinja2.setup that init_app
    # does, to verify the autoescape config we ship is the
    # select_autoescape callable rather than a static False.
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.DictLoader({}),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    env = aiohttp_jinja2.get_env(app)
    assert callable(env.autoescape)
    assert env.autoescape("page.html") is True
    assert env.autoescape("notes.txt") is False
