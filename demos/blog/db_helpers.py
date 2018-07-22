from sqlalchemy import create_engine, MetaData

from aiohttpdemo_blog.db import construct_db_url
from aiohttpdemo_blog.db import users, posts
from aiohttpdemo_blog.security import generate_password_hash
from aiohttpdemo_blog.settings import load_config


def setup_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)

    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']
    db_pass = target_config['DB_PASS']

    with engine.connect() as conn:
        teardown_db(executor_config=executor_config,
                    target_config=target_config)

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


def create_tables(target_config=None):
    engine = get_engine(target_config)

    meta = MetaData()
    meta.create_all(bind=engine, tables=[users, posts])


def drop_tables(target_config=None):
    engine = get_engine(target_config)

    meta = MetaData()
    meta.drop_all(bind=engine, tables=[users, posts])


def create_sample_data(target_config=None):
    engine = get_engine(target_config)

    with engine.connect() as conn:
        conn.execute(users.insert(), [
            {'username': 'Adam',
             'email': 'adam@one.com',
             'password_hash': generate_password_hash('adam')},
            {'username': 'Bob',
             'email': 'bob@two.com',
             'password_hash': generate_password_hash('bob')},
        ])
        conn.execute(posts.insert(), [
            {'user_id': 1, 'body': 'Lovely day'},
            {'user_id': 2, 'body': 'Roses are red'},
            {'user_id': 2, 'body': 'Lorem ipsum'},
        ])


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
        setup_db(executor_config=admin_db_config,
                 target_config=user_db_config)
    elif args.drop:
        teardown_db(executor_config=admin_db_config,
                    target_config=user_db_config)
    elif args.recreate:
        teardown_db(executor_config=admin_db_config,
                    target_config=user_db_config)
        setup_db(executor_config=admin_db_config,
                 target_config=user_db_config)
    elif args.all:
        teardown_db(executor_config=admin_db_config,
                    target_config=user_db_config)
        setup_db(executor_config=admin_db_config,
                 target_config=user_db_config)
        create_tables(target_config=user_db_config)
        create_sample_data(target_config=user_db_config)
    else:
        parser.print_help()
