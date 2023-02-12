import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from aiohttpdemo_blog.db import construct_db_url
from aiohttpdemo_blog.db import Users, Posts, Base
from aiohttpdemo_blog.security import generate_password_hash
from aiohttpdemo_blog.settings import load_config


async def setup_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)
    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']
    db_pass = target_config['DB_PASS']

    async with engine.connect() as conn:
        await conn.execute(text("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass)))
        await conn.execute(text("CREATE DATABASE %s" % db_name))
        await conn.execute(text("ALTER DATABASE %s OWNER TO %s" % (db_name, db_user)))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO %s" % db_user))
        await conn.commit()

    await engine.dispose()


async def teardown_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)
    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']

    async with engine.connect() as conn:
        # terminate all connections to be able to drop database
        await conn.execute(text("""
          SELECT pg_terminate_backend(pg_stat_activity.pid)
          FROM pg_stat_activity
          WHERE pg_stat_activity.datname = '%s'
            AND pid <> pg_backend_pid();""" % db_name))
        await conn.execute(text("DROP DATABASE IF EXISTS %s" % db_name))
        await conn.execute(text("REVOKE ALL ON SCHEMA public FROM %s" % db_user))
        await conn.execute(text("DROP ROLE IF EXISTS %s" % db_user))
        await conn.commit()
    
    await engine.dispose()

def get_engine(db_config):
    db_url = construct_db_url(db_config)
    engine = create_async_engine(db_url, isolation_level='AUTOCOMMIT')
    return engine


async def create_tables(target_config=None):
    engine = get_engine(target_config)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

async def drop_tables(target_config=None):
    engine = get_engine(target_config)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

async def create_sample_data(target_config=None):
    engine = get_engine(target_config)
    Session = async_sessionmaker(engine)

    async with Session.begin() as sess:
        sess.add_all((
            Users(username="Adam", email="adam@one.com",
                  password_hash=generate_password_hash("adam")),
            Users(username="Bob", email="bob@two.com",
                  password_hash=generate_password_hash("bob")),
            Posts(user_id=1, body="Lovely day"),
            Posts(user_id=2, body="Roses are red"),
            Posts(user_id=2, body="Lorem ipsum")
        ))
        
    await engine.dispose()


if __name__ == '__main__':
    user_db_config = load_config('config/user_config.toml')['database']
    admin_db_config = load_config('config/admin_config.toml')['database']

    import argparse
    parser = argparse.ArgumentParser(description='DB related shortcuts')
    parser.add_argument("-c", "--create",
                        help="Create empty database and user with permissions",
                        action='store_true')
    parser.add_argument("-d", "--drop",
                        help="Drop database and user role",
                        action='store_true')
    parser.add_argument("-r", "--recreate",
                        help="Drop and recreate database and user",
                        action='store_true')
    parser.add_argument("-a", "--all",
                        help="Create sample data",
                        action='store_true')
    args = parser.parse_args()

    if args.create:
        asyncio.run(setup_db(executor_config=admin_db_config,
                 target_config=user_db_config))
    elif args.drop:
        asyncio.run(teardown_db(executor_config=admin_db_config,
                    target_config=user_db_config))
    elif args.recreate:
        asyncio.run(teardown_db(executor_config=admin_db_config,
                    target_config=user_db_config))
        asyncio.run(setup_db(executor_config=admin_db_config,
                 target_config=user_db_config))
    elif args.all:
        asyncio.run(teardown_db(executor_config=admin_db_config,
                    target_config=user_db_config))
        asyncio.run(setup_db(executor_config=admin_db_config,
                 target_config=user_db_config))
        asyncio.run(create_tables(target_config=user_db_config))
        asyncio.run(create_sample_data(target_config=user_db_config))
    else:
        parser.print_help()
