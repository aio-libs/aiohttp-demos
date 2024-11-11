# aiohttpdemo_polls/db.py
from datetime import date

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_text: Mapped[str] = mapped_column(String(200), nullable=False)
    pub_date: Mapped[date]


class Choice(Base):
    __tablename__ = "choice"

    id: Mapped[int] = mapped_column(primary_key=True)
    choice_text: Mapped[str] = mapped_column(String(200), nullable=False)
    votes: Mapped[int] = mapped_column(server_default="0", nullable=False)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE")
    )


class RecordNotFound(Exception):
    """Requested record in database was not found"""


DSN = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


async def pg_context(app):
    engine = create_async_engine(DSN.format(**app["config"]["postgres"]))
    app["db"] = async_sessionmaker(engine)

    yield

    await engine.dispose()


async def get_question(sess, question_id):
    result = await sess.scalars(select(Question).where(Question.id == question_id))
    question_record = result.first()
    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))
    result = await sess.scalars(
        select(Choice).where(Choice.question_id == question_id).order_by(Choice.id)
    )
    choice_records = result.all()
    return question_record, choice_records


async def vote(app, question_id, choice_id):
    async with app["db"].begin() as sess:
        result = await sess.get(Choice, choice_id)
        result.votes += 1
        if not result:
            msg = "Question with id: {} or choice id: {} does not exists"
            raise RecordNotFound(msg.format(question_id, choice_id))
