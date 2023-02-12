# polls/init_db.py
import asyncio
from datetime import date

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from aiohttpdemo_polls.db import Question, Choice, Base
from aiohttpdemo_polls.settings import BASE_DIR, get_config

DSN = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

ADMIN_DB_URL = DSN.format(
    user='postgres', password='postgres', database='postgres',
    host='localhost', port=5432
)
admin_engine = create_async_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')

USER_CONFIG_PATH = BASE_DIR / 'config' / 'polls.yaml'
USER_CONFIG = get_config(['-c', USER_CONFIG_PATH.as_posix()])
USER_DB_URL = DSN.format(**USER_CONFIG['postgres'])
user_engine = create_async_engine(USER_DB_URL)

TEST_CONFIG_PATH = BASE_DIR / 'config' / 'polls_test.yaml'
TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
TEST_DB_URL = DSN.format(**TEST_CONFIG['postgres'])
test_engine = create_async_engine(TEST_DB_URL)


async def create_tables(engine=test_engine):
    Session = async_sessionmaker(engine)
    async with Session.begin() as sess:
        await sess.run_sync(Base.metadata.create_all)
    

async def sample_data(engine=test_engine):
    Session = async_sessionmaker(engine)
    async with Session.begin() as sess:
        sess.add_all((
            Question(question_text="What\'s new?",pub_date=date(2015, 12, 15)),
            Choice(choice_text="Not much", votes=0, question_id=1),
            Choice(choice_text="The sky", votes=0, question_id=1),
            Choice(choice_text="Just hacking again", votes=0, question_id=1)
        ))

if __name__ == "__main__":
    asyncio.run(create_tables(engine=user_engine))
    asyncio.run(sample_data(engine=user_engine))