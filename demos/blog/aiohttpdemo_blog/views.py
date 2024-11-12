import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import remember, forget, authorized_userid

from aiohttpdemo_blog import db
from aiohttpdemo_blog.forms import validate_login_form
from aiohttpdemo_blog.typedefs import db_key


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)


@aiohttp_jinja2.template('index.html')
async def index(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    async with request.app[db_key]() as sess:
        current_user = await db.get_user_by_name(sess, username)
        posts = await db.get_posts_with_joined_users(sess)

    return {'user': current_user, 'posts': posts}


@aiohttp_jinja2.template('login.html')
async def login(request):
    username = await authorized_userid(request)
    if username:
        raise redirect(request.app.router, 'index')

    if request.method == 'POST':
        form = await request.post()

        async with request.app[db_key]() as sess:
            error = await validate_login_form(sess, form)

            if error:
                return {'error': error}
            else:
                response = redirect(request.app.router, 'index')

                user = await db.get_user_by_name(sess, form['username'])
                await remember(request, response, user.username)

                raise response

    return {}


async def logout(request):
    response = redirect(request.app.router, 'login')
    await forget(request, response)
    return response


@aiohttp_jinja2.template('create_post.html')
async def create_post(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    if request.method == 'POST':
        form = await request.post()

        async with request.app[db_key].begin() as sess:
            current_user = await db.get_user_by_name(sess, username)
            sess.add(db.Posts(body=form["body"], user_id=current_user.id))
            raise redirect(request.app.router, 'index')

    return {}
