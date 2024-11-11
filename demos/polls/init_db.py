import asyncio
from datetime import date

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from aiohttpdemo_polls.db import Base, Choice, Question
from aiohttpdemo_polls.settings import BASE_DIR, get_config

DSN = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

ADMIN_DB_URL = DSN.format(
    user="postgres",
    password="postgres",
    database="postgres",
    host="localhost",
    port=5432,
)
admin_engine = create_async_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")

USER_CONFIG_PATH = BASE_DIR / "config" / "polls.yaml"
USER_CONFIG = get_config(["-c", USER_CONFIG_PATH.as_posix()])
USER_DB_URL = DSN.format(**USER_CONFIG["postgres"])
user_engine = create_async_engine(USER_DB_URL)


async def setup_db(config):
    db_name = config["database"]
    db_user = config["user"]
    db_pass = config["password"]

    async with admin_engine.connect() as conn:
        await conn.execute(text("DROP DATABASE IF EXISTS %s" % db_name))
        await conn.execute(
            text("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
        )
        await conn.execute(text("CREATE DATABASE %s ENCODING 'UTF8'" % db_name))
        await conn.execute(text("ALTER DATABASE %s OWNER TO %s" % (db_name, db_user)))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO %s" % db_user))
        await conn.commit()


async def teardown_db(config):
    db_name = config["database"]
    db_user = config["user"]

    async with admin_engine.connect() as conn:
        await conn.execute(
            text(
                """
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '%s'
                AND pid <> pg_backend_pid();"""
                % db_name
            )
        )
        await conn.execute(text("DROP DATABASE IF EXISTS %s" % db_name))
        await conn.execute(text("REVOKE ALL ON SCHEMA public FROM %s" % db_user))
        await conn.execute(text("DROP ROLE IF EXISTS %s" % db_user))
        await conn.commit()


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def drop_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


async def sample_data(engine):
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session.begin() as sess:
        q = Question(question_text="What's new?", pub_date=date(2015, 12, 15))
        sess.add(q)
    async with Session.begin() as sess:
        sess.add_all(
            (
                Choice(choice_text="Not much", votes=0, question_id=q.id),
                Choice(choice_text="The sky", votes=0, question_id=q.id),
                Choice(choice_text="Just hacking again", votes=0, question_id=q.id),
            )
        )


if __name__ == "__main__":
    asyncio.run(setup_db(USER_CONFIG["postgres"]))
    asyncio.run(create_tables(engine=user_engine))
    asyncio.run(sample_data(engine=user_engine))
    # drop_tables()
    # teardown_db(USER_CONFIG['postgres'])
