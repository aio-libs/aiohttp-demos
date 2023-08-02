from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from graph.auth.tables import Users
from graph.db import Base

class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

    # ForeignKey
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("Users.id", ondelete="CASCADE"))

class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    body: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    who_like: Mapped[list[int]] = mapped_column(server_default="{}")

    # ForeignKey
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(
        ForeignKey(Rooms.id, ondelete="CASCADE"))
