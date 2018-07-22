from datetime import datetime as dt

import asyncpgsa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)
from sqlalchemy.sql import select

metadata = MetaData()


users = Table(
    'users', metadata,

    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('email', String(120)),
    Column('password_hash', String(128), nullable=False)
)


posts = Table(
    'posts', metadata,

    Column('id', Integer, primary_key=True),
    Column('body', String(140)),
    Column('timestamp', DateTime, index=True, default=dt.utcnow),

    Column('user_id',
           Integer,
           ForeignKey('users.id'))
)


async def init_db(app):
    dsn = construct_db_url(app['config']['database'])
    pool = await asyncpgsa.create_pool(dsn=dsn)
    app['db_pool'] = pool
    return pool


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )


async def get_user_by_name(conn, username):
    result = await conn.fetchrow(
        users
        .select()
        .where(users.c.username == username)
    )
    return result


async def get_users(conn):
    records = await conn.fetch(
        users.select().order_by(users.c.id)
    )
    return records


async def get_posts(conn):
    records = await conn.fetch(
        posts.select().order_by(posts.c.id)
    )
    return records


async def get_posts_with_joined_users(conn):
    j = posts.join(users, posts.c.user_id == users.c.id)
    stmt = select(
        [posts, users.c.username]).select_from(j).order_by(posts.c.timestamp)
    records = await conn.fetch(stmt)
    return records


async def create_post(conn, post_body, user_id):
    stmt = posts.insert().values(body=post_body, user_id=user_id)
    await conn.execute(stmt)
