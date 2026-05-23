import aiohttp_jinja2
import jinja2
import pytest
from aiohttp import web

from motortwit.main import setup_jinja
from motortwit.security import AuthorizationPolicy


class _DummyMongo:
    """Fail loudly if any DB access happens during these tests."""

    def __getattr__(self, _name):
        raise AssertionError("mongo should not be accessed for malformed IDs")


@pytest.mark.parametrize("identity", [
    "not-an-objectid",
    "short",
    "",
    None,
    "x" * 24,  # right length, wrong alphabet
])
async def test_authorized_userid_returns_none_for_malformed_identity(identity):
    policy = AuthorizationPolicy(_DummyMongo())
    assert await policy.authorized_userid(identity) is None


def test_jinja_setup_enables_explicit_autoescape():
    app = web.Application()
    setup_jinja(app)
    env = aiohttp_jinja2.get_env(app)

    assert callable(env.autoescape), (
        "autoescape should be a select_autoescape callable, "
        "not the default heuristic"
    )
    assert env.autoescape("page.html") is True
    assert env.autoescape("config.xml") is True
    assert env.autoescape("notes.txt") is False


def test_jinja_autoescape_escapes_html_in_rendered_template(tmp_path):
    template_path = tmp_path / "x.html"
    template_path.write_text("{{ value }}")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(tmp_path)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    rendered = env.get_template("x.html").render(value="<script>alert(1)</script>")
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
