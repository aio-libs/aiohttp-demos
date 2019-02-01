import datetime

import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid, forget, remember
from bson import ObjectId

from . import db
from .security import (auth_required, check_password_hash,
                       generate_password_hash)
from .utils import redirect, validate_register_form


class SiteHandler:

    def __init__(self, mongo):
        self._mongo = mongo

    @property
    def mongo(self):
        return self._mongo

    @aiohttp_jinja2.template('timeline.html')
    async def timeline(self, request):
        user_id = await authorized_userid(request)

        if user_id is None:
            router = request.app.router
            location = router['public_timeline'].url_for()
            raise web.HTTPFound(location=location)

        user = await self.mongo.user.find_one({'_id': ObjectId(user_id)})

        query = {'who_id': ObjectId(user_id)}
        filter = {'whom_id': 1}
        followed = await self.mongo.follower.find_one(query, filter)
        if followed is None:
            followed = {'whom_id': []}

        query = {'$or': [{'author_id': ObjectId(user_id)},
                         {'author_id': {'$in': followed['whom_id']}}]}
        messages = await (self.mongo.message
                          .find(query)
                          .sort('pub_date', -1)
                          .to_list(30))
        endpoint = request.match_info.route.name
        return {'messages': messages,
                'user': user,
                'endpoint': endpoint}

    @aiohttp_jinja2.template('timeline.html')
    async def public_timeline(self, request):
        messages = await (self.mongo.message
                          .find()
                          .sort('pub_date', -1)
                          .to_list(30))
        return {'messages': messages,
                'endpoint': request.match_info.route.name}

    @aiohttp_jinja2.template('timeline.html')
    async def user_timeline(self, request):
        username = request.match_info['username']
        profile_user = await self.mongo.user.find_one({'username': username})
        if profile_user is None:
            raise web.HTTPNotFound()

        followed = False
        user_id = await authorized_userid(request)
        user = None
        if user_id:
            user = await self.mongo.user.find_one({'_id': ObjectId(user_id)})
            followed = await self.mongo.follower.find_one(
                {'who_id': ObjectId(user_id),
                 'whom_id': {'$in': [ObjectId(profile_user['_id'])]}})
            followed = followed is not None

        messages = await (self.mongo.message
                          .find({'author_id': ObjectId(profile_user['_id'])})
                          .sort('pub_date', -1)
                          .to_list(30))

        profile_user['_id'] = str(profile_user['_id'])
        return {'messages': messages,
                'followed': followed,
                'profile_user': profile_user,
                'user': user,
                'endpoint': request.match_info.route.name}

    @aiohttp_jinja2.template('login.html')
    async def login(self, request):
        form = await request.post()
        user = await self.mongo.user.find_one({'username': form['username']})

        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'], form['password']):
            error = 'Invalid password'
        else:
            response = redirect(request, 'timeline')
            await remember(request, response, str(user['_id']))
            return response

        return {'error': error, 'form': form}

    @aiohttp_jinja2.template('login.html')
    async def login_page(self, request):
        return {'error': None, 'form': None}

    async def logout(self, request):
        response = redirect(request, 'public_timeline')
        await forget(request, response)
        return response

    @aiohttp_jinja2.template('register.html')
    async def register(self, request):
        user_id = await authorized_userid(request)
        if user_id:
            return redirect(request, 'timeline')

        form = await request.post()
        error = await validate_register_form(self.mongo, form)

        if error is None:
            await self.mongo.user.insert_one(
                {'username': form['username'],
                 'email': form['email'],
                 'pw_hash': generate_password_hash(form['password'])})
            return redirect(request, 'login')
        return {'error': error, 'form': form}

    @aiohttp_jinja2.template('register.html')
    async def register_page(self, request):
        user_id = await authorized_userid(request)
        if user_id:
            return redirect(request, 'timeline')
        return {'error': None, 'form': None}

    @auth_required
    async def follow_user(self, request):
        username = request.match_info['username']
        user_id = await authorized_userid(request)

        whom_id = await db.get_user_id(self.mongo.user, username)

        if whom_id is None:
            raise web.HTTPFound()

        await self.mongo.follower.update(
            {'who_id': ObjectId(user_id)},
            {'$push': {'whom_id': whom_id}}, upsert=True)

        return redirect(request, 'user_timeline', parts={'username': username})

    @auth_required
    async def unfollow_user(self, request):
        username = request.match_info['username']
        user_id = await authorized_userid(request)

        whom_id = await db.get_user_id(self.mongo.user, username)
        if whom_id is None:
            raise web.HTTPFound()

        await self.mongo.follower.update(
            {'who_id': ObjectId(user_id)},
            {'$pull': {'whom_id': whom_id}})
        return redirect(request, 'user_timeline', parts={'username': username})

    @auth_required
    async def add_message(self, request):
        user_id = await authorized_userid(request)
        form = await request.post()

        if form.get('text'):
            user = await self.mongo.user.find_one(
                {'_id': ObjectId(user_id)},
                {'email': 1, 'username': 1})

            await self.mongo.message.insert_one(
                {'author_id': ObjectId(user_id),
                 'email': user['email'],
                 'username': user['username'],
                 'text': form['text'],
                 'pub_date': datetime.datetime.utcnow()})
        return redirect(request, 'timeline')
