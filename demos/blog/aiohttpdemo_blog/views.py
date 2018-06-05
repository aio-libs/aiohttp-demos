import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import remember, forget, authorized_userid

from aiohttpdemo_blog.models import User, Post
from aiohttpdemo_blog.forms import validate_login_form


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)


@aiohttp_jinja2.template('index.html')
async def index(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    current_user = await User.query.where(User.username == username).gino.first()
    posts = await Post.query.gino.all()

    return {'user': current_user, 'posts': posts}


@aiohttp_jinja2.template('login.html')
async def login(request):
    username = await authorized_userid(request)
    if username:
        raise redirect(request.app.router, 'index')

    if request.method == 'POST':
        form = await request.post()

        error = await validate_login_form(form)
        if error:
            return {'error': error}
        else:
            response = redirect(request.app.router, 'index')

            user = await User.query.where(User.username == form['username']).gino.first()
            await remember(request, response, user.username)

            raise response


    return {}


async def logout(request):
    response = redirect(request.app.router, 'login')
    await forget(request, response)
    return response
