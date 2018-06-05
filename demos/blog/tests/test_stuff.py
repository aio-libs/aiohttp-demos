from aiohttpdemo_blog.security import generate_password_hash, check_password_hash
from aiohttpdemo_blog.forms import validate_login_form

from aiohttpdemo_blog.models import User, Post


def test_security():
    user_password = 'qwer'
    hashed = generate_password_hash(user_password)
    assert check_password_hash(user_password, hashed)


async def test_creation_with_gino(tables_and_data, gino_db):
    assert 2 == await gino_db.func.count(User.id).gino.scalar()

    await User.create(username='Clark',
                      password_hash=generate_password_hash('clark'))

    assert 3 == await gino_db.func.count(User.id).gino.scalar()


async def test_login_form(tables_and_data):
    invalid_form = {
        'username': 'Joe',
        'password': '123'
    }
    valid_form = {
        'username': 'Adam',
        'password': 'adam'
    }

    error = await validate_login_form(invalid_form)
    assert error

    no_error = await validate_login_form(valid_form)
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
