import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import login_required
from aiohttp_security import remember, authorized_userid

from db import User, Post
from forms import validate_login_form


@login_required
@aiohttp_jinja2.template('index.html')
async def index(request):
    username = await authorized_userid(request)
    current_user = await User.query.where(User.username == username).gino.first()
    posts = await Post.query.gino.all()
    return {'user': current_user, 'posts': posts}


@aiohttp_jinja2.template('login.html')
async def login(request):

    if request.method == 'POST':
        form = await request.post()

        error = await validate_login_form(form)
        if error:
            return {'error': error}
        else:
            location = request.app.router['index'].url_for()
            response = web.HTTPFound(location=location)

            user = await User.query.where(User.username == form['username']).gino.first()
            await remember(request, response, user.username)

            raise response


    return {}
