from graph.auth.enums import UserGender
from graph.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(200), unique=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(10))
    avatar_url = Mapped[str]
    gender: Mapped[UserGender] = mapped_column(server_default=UserGender.none.value)
