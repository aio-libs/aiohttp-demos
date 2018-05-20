from db import User


def validate_password(form_pass, user):
    # TODO: check agains stored password hash
    return True


async def validate_login_form(form):
    error = None

    username = form['username']
    password = form['password']

    if not username:
        return 'username is required'
    if not password:
        return 'password is required'

    user = await User.query.where(User.username == username).gino.first()
    if not user:
        return 'Invalid username'
    if not validate_password(password, user):
        return 'Invalid password'
    else:
        return None

    return 'error'
