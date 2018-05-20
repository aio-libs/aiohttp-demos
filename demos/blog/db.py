import asyncio
from gino import Gino
from datetime import datetime as dt


db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User `{self.username}`>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post `{self.body}`>'


async def setup_db(db_url):
    await db.set_bind(db_url)



# =================================

async def create_sample_data():
    await User.create(username='Adam', email='adam@one.com')
    await User.create(username='Bob', email='bob@two.com')

    u1 = await User.query.where(User.username == 'Adam').gino.first()
    u2 = await User.query.where(User.username == 'Bob').gino.first()

    await Post.create(user_id=u1.id, body='Lovely day')
    await Post.create(user_id=u1.id, body='Roses are red')
    await Post.create(user_id=u2.id, body='Lorem ipsum')


async def delete_sample_data():
    await Post.delete.gino.status()
    await User.delete.gino.status()


if __name__ == '__main__':
    from db_helpers import construct_db_url
    from config import user_config, admin_config

    DB_URL = construct_db_url(user_config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.set_bind(DB_URL))

    loop.run_until_complete(db.gino.create_all())

    loop.run_until_complete(create_sample_data())
    # loop.run_until_complete(delete_sample_data())
