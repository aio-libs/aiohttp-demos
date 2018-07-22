from aiohttpdemo_blog import db
from aiohttpdemo_blog.security import check_password_hash


async def validate_login_form(conn, form):

    username = form['username']
    password = form['password']

    if not username:
        return 'username is required'
    if not password:
        return 'password is required'

    user = await db.get_user_by_name(conn, username)

    if not user:
        return 'Invalid username'
    if not check_password_hash(password, user['password_hash']):
        return 'Invalid password'
    else:
        return None

    return 'error'
