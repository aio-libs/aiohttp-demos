from aiohttpdemo_blog.forms import validate_login_form
from aiohttpdemo_blog.security import (
    generate_password_hash,
    check_password_hash
)


def test_security():
    user_password = 'qwer'
    hashed = generate_password_hash(user_password)
    assert check_password_hash(user_password, hashed)


async def test_index_view(tables_and_data, client):
    resp = await client.get('/')
    assert resp.status == 200


async def test_login_form(tables_and_data, client):
    invalid_form = {
        'username': 'Joe',
        'password': '123'
    }
    valid_form = {
        'username': 'Adam',
        'password': 'adam'
    }

    async with client.server.app['db_pool'].acquire() as conn:
        error = await validate_login_form(conn, invalid_form)
        assert error

        no_error = await validate_login_form(conn, valid_form)
        assert not no_error


async def test_login_view(tables_and_data, client):
    invalid_form = {
        'username': 'Joe',
        'password': '123'
    }
    valid_form = {
        'username': 'Adam',
        'password': 'adam'
    }

    resp = await client.post('/login', data=invalid_form)
    assert resp.status == 200
    assert 'Invalid username' in await resp.text()

    resp = await client.post('/login', data=valid_form)
    assert resp.status == 200
    assert 'Hi, Adam!' in await resp.text()
