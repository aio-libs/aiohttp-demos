from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy import ARRAY, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from graph.auth.models import User
from graph.db import Base

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

    # ForeignKey
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    body: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    who_like: Mapped[list[int]] = mapped_column(ARRAY(Integer), server_default="{}")

    # ForeignKey
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey(Room.id, ondelete="CASCADE"))
