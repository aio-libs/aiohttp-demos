import aiopg.sa
import sqlalchemy as sa
from sqlalchemy.sql import select

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey


__all__ = ['question', 'choice']

meta = sa.MetaData()

Base = declarative_base()


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question_text = Column(String(200), nullable=False)
    pub_date = Column(Date, nullable=False)


class Choice(Base):
    __tablename__ = 'choice'

    id = Column(Integer, primary_key=True)
    choice_text = Column(String(200), nullable=False)
    votes = Column(Integer, server_default="0", nullable=False)

    question_id = Column(Integer,
                         ForeignKey('question.id', ondelete='CASCADE'))


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_question(conn, question_id):
    result = await conn.execute(
        select([Question])
        .where(Question.id == question_id))
    question_record = await result.first()
    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))
    result = await conn.execute(
        select([Choice])
        .where(Choice.question_id == question_id)
        .order_by(Choice.id))
    choice_recoreds = await result.fetchall()
    return question_record, choice_recoreds


async def vote(conn, question_id, choice_id):
    result = await conn.execute(
        choice.update()
        .returning(*choice.c)
        .where(choice.c.question_id == question_id)
        .where(choice.c.id == choice_id)
        .values(votes=choice.c.votes+1))
    record = await result.fetchone()
    if not record:
        msg = "Question with id: {} or choice id: {} does not exists"
        raise RecordNotFound(msg.format(question_id, choice_id))
