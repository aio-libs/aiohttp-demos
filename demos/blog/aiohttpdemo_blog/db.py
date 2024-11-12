from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.sql import select

from aiohttpdemo_blog.typedefs import config_key, db_key


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    posts: Mapped[list["Posts"]] = relationship(
        back_populates="user", lazy="raise_on_sql"
    )


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(140))
    timestamp: Mapped[datetime] = mapped_column(index=True, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Users] = relationship(back_populates="posts", lazy="raise_on_sql")


async def init_db(app):
    dsn = construct_db_url(app[config_key]["database"])
    engine = create_async_engine(dsn)
    app[db_key] = async_sessionmaker(engine)

    yield

    await engine.dispose()


def construct_db_url(config):
    DSN = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config["DB_USER"],
        password=config["DB_PASS"],
        database=config["DB_NAME"],
        host=config["DB_HOST"],
        port=config["DB_PORT"],
    )


async def get_user_by_name(sess, username):
    result = await sess.scalar(select(Users).where(Users.username == username))
    return result


async def get_users(sess):
    records = await sess.scalars(select(Users).order_by(Users.id))
    return records.all()


async def get_posts(sess):
    records = await sess.scalars(select(Posts).order_by(Posts.id))
    return records.all()


async def get_posts_with_joined_users(sess):
    records = await sess.scalars(
        select(Posts).options(selectinload(Posts.user)).order_by(Posts.timestamp)
    )
    return records.all()
