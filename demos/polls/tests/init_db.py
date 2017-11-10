from sqlalchemy import create_engine, MetaData
from aiohttpdemo_polls.db import question, choice

from aiohttpdemo_polls.config import DB_CONFIG_ADMIN, DB_CONFIG_USER


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

DB_URL = DSN.format(**DB_CONFIG_ADMIN)
engine = create_engine(DB_URL, isolation_level='AUTOCOMMIT')

DB_URL_USER = DSN.format(**DB_CONFIG_USER)
engine_user = create_engine(DB_URL_USER)


def setup_db(db_name, db_user, db_pass):
    conn = engine.connect()
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute("CREATE DATABASE %s ENCODING 'UTF8'" % db_name)
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" % (db_name, db_user))
    conn.close()


def teardown_db(db_name, db_user):
    conn = engine.connect()
    conn.execute("""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '%s'
        AND pid <> pg_backend_pid();""" % db_name)
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.close()


def create_tables():
    meta = MetaData()
    meta.create_all(bind=engine_user, tables=[question, choice])

def drop_tables():
    meta = MetaData()
    meta.drop_all(bind=engine_user, tables=[question, choice])


def sample_data():
    conn = engine_user.connect()
    conn.execute(question.insert(), [
        {'question_text': 'What\'s new?', 'pub_date': '2015-12-15 17:17:49.629+02'}
    ])
    conn.execute(choice.insert(), [
        {'choice_text': 'Not much', 'votes': 0, 'question_id': 1},
        {'choice_text': 'The sky', 'votes': 0, 'question_id': 1},
        {'choice_text': 'Just hacking again', 'votes': 0, 'question_id': 1},
    ])
    conn.close()


if __name__ == '__main__':

    db_name = DB_CONFIG_USER['database']
    db_user = DB_CONFIG_USER['user']
    db_pass = DB_CONFIG_USER['password']

    setup_db(db_name, db_user, db_pass)
    create_tables()
    sample_data()
    drop_tables()
    teardown_db(db_name, db_user)
