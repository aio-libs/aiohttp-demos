# polls/init_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from aiohttpdemo_polls.db import Question, Choice, Base
from aiohttpdemo_polls.settings import BASE_DIR, get_config

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

ADMIN_DB_URL = DSN.format(
    user='postgres', password='postgres', database='postgres',
    host='localhost', port=5432
)
admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')

USER_CONFIG_PATH = BASE_DIR / 'config' / 'polls.yaml'
USER_CONFIG = get_config(['-c', USER_CONFIG_PATH.as_posix()])
USER_DB_URL = DSN.format(**USER_CONFIG['postgres'])
user_engine = create_engine(USER_DB_URL)

TEST_CONFIG_PATH = BASE_DIR / 'config' / 'polls_test.yaml'
TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
TEST_DB_URL = DSN.format(**TEST_CONFIG['postgres'])
test_engine = create_engine(TEST_DB_URL)


def create_tables(engine=test_engine):
    Base.metadata.create_all(bind=engine)

def sample_data(engine=test_engine):
    Session = sessionmaker(engine)
    with Session.begin() as session:
        session.add_all((
            Question(question_text="What\'s new?",pub_date=date(2015, 12, 15)),
            Choice(choice_text="Not much", votes=0, question_id=1),
            Choice(choice_text="The sky", votes=0, question_id=1),
            Choice(choice_text="Just hacking again", votes=0, question_id=1)
        ))

if __name__ == "__main__":
    create_tables(engine=user_engine)
    sample_data(engine=user_engine)