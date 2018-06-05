from aiohttpdemo_blog.models import User, Post
from aiohttpdemo_blog.models import construct_db_url
from aiohttpdemo_blog.security import generate_password_hash
from aiohttpdemo_blog.settings import load_config
from sqlalchemy import create_engine


def setup_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)

    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']
    db_pass = target_config['DB_PASS']

    with engine.connect() as conn:
        teardown_db(executor_config=executor_config, target_config=target_config)

        conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
        conn.execute("CREATE DATABASE %s" % db_name)
        conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                     (db_name, db_user))


def teardown_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)

    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']

    with engine.connect() as conn:
        # terminate all connections to be able to drop database
        conn.execute("""
          SELECT pg_terminate_backend(pg_stat_activity.pid)
          FROM pg_stat_activity
          WHERE pg_stat_activity.datname = '%s'
            AND pid <> pg_backend_pid();""" % db_name)
        conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
        conn.execute("DROP ROLE IF EXISTS %s" % db_user)


def get_engine(db_config):
    db_url = construct_db_url(db_config)
    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    return engine


async def create_tables(gino_db):
    await gino_db.gino.create_all()


async def drop_tables(gino_db):
    await gino_db.gino.drop_all()


async def create_sample_data():
    await User.create(username='Adam',
                      email='adam@one.com',
                      password_hash=generate_password_hash('adam'))
    await User.create(username='Bob',
                      email='bob@two.com',
                      password_hash=generate_password_hash('bob'))

    u1 = await User.query.where(User.username == 'Adam').gino.first()
    u2 = await User.query.where(User.username == 'Bob').gino.first()

    await Post.create(user_id=u1.id, body='Lovely day')
    await Post.create(user_id=u1.id, body='Roses are red')
    await Post.create(user_id=u2.id, body='Lorem ipsum')


if __name__ == '__main__':
    user_db_config = load_config('config/user_config.toml')['database']
    admin_db_config = load_config('config/admin_config.toml')['database']

    import argparse
    parser = argparse.ArgumentParser(description='DB related shortcuts')
    parser.add_argument("-c", "--create", help="Create empty database and user with permissions", action='store_true')
    parser.add_argument("-d", "--drop", help="Drop database and user role", action='store_true')
    parser.add_argument("-r", "--recreate", help="Drop and recreate database and user", action='store_true')
    parser.add_argument("-a", "--all", help="Create sample data", action='store_true')
    args = parser.parse_args()

    if args.create:
        setup_db(executor_config=admin_db_config, target_config=user_db_config)
    elif args.drop:
        teardown_db(executor_config=admin_db_config, target_config=user_db_config)
    elif args.recreate:
        teardown_db(executor_config=admin_db_config, target_config=user_db_config)
        setup_db(executor_config=admin_db_config, target_config=user_db_config)
    elif args.all:
        teardown_db(executor_config=admin_db_config, target_config=user_db_config)
        setup_db(executor_config=admin_db_config, target_config=user_db_config)

        import asyncio
        from aiohttpdemo_blog.models import db as gino_db
        loop = asyncio.get_event_loop()

        db_url = construct_db_url(user_db_config)
        loop.run_until_complete(gino_db.set_bind(db_url))
        loop.run_until_complete(create_tables(gino_db))
        loop.run_until_complete(create_sample_data())
    else:
        parser.print_help()
