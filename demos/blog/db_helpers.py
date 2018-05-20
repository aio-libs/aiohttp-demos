def setup_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)

    db_name = target_config.DB_NAME
    db_user = target_config.DB_USER
    db_pass = target_config.DB_PASS

    with engine.connect() as conn:
        teardown_db(executor_config=executor_config, target_config=target_config)

        conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
        conn.execute("CREATE DATABASE %s" % db_name)
        conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                     (db_name, db_user))


def teardown_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)

    db_name = target_config.DB_NAME
    db_user = target_config.DB_USER

    with engine.connect() as conn:
        # terminate all connections to be able to drop database
        conn.execute("""
          SELECT pg_terminate_backend(pg_stat_activity.pid)
          FROM pg_stat_activity
          WHERE pg_stat_activity.datname = '%s'
            AND pid <> pg_backend_pid();""" % db_name)
        conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
        conn.execute("DROP ROLE IF EXISTS %s" % db_user)


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        host=config.DB_HOST,
        port=config.DB_PORT
    )


def get_engine(config):
    from sqlalchemy import create_engine

    db_url = construct_db_url(config)
    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    return engine


if __name__ == '__main__':
    import argparse
    from config import user_config, admin_config

    parser = argparse.ArgumentParser(description='DB related shortcuts')
    parser.add_argument("-c", "--create", help="Create empty database and user with permissions", action='store_true')
    parser.add_argument("-d", "--drop", help="Drop database and user role", action='store_true')
    parser.add_argument("-r", "--recreate", help="Drop and recreate database and user", action='store_true')
    args = parser.parse_args()

    if args.create:
        setup_db(executor_config=admin_config, target_config=user_config)
    elif args.drop:
        teardown_db(executor_config=admin_config, target_config=user_config)
    elif args.recreate:
        teardown_db(executor_config=admin_config, target_config=user_config)
        setup_db(executor_config=admin_config, target_config=user_config)
    else:
        parser.print_help()
