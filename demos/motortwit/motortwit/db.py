import trafaret as t
from trafaret.contrib.object_id import MongoId
from trafaret.contrib.rfc_3339 import DateTime


user = t.Dict({
    t.Key('_id'): MongoId(),
    t.Key('username'): t.String(max_length=50),
    t.Key('email'): t.Email,
    t.Key('pw_hash'): t.String(),
})


message = t.Dict({
    t.Key('_id'): MongoId(),
    t.Key('author_id'): MongoId(),
    t.Key('username'): t.String(max_length=50),
    t.Key('text'): t.String(),
    t.Key('pub_date'): DateTime(),
})

follower = t.Dict({
    t.Key('_id'): MongoId(),
    t.Key('who_id'): MongoId(),
    t.Key('whom_id'): t.List(MongoId()),
})


async def get_user_id(user_collection, username):
    rv = await (user_collection.find_one(
        {'username': username},
        {'_id': 1}))
    return rv['_id'] if rv else None
