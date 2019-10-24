from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa

from graph.db import metadata
from graph.auth.tables import users


__all__ = ['rooms', 'messages', ]


rooms = sa.Table(
    'rooms', metadata,

    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('name', sa.String(20), unique=True),

    # ForeignKey
    sa.Column(
        'owner_id',
        sa.ForeignKey(users.c.id, ondelete='CASCADE'),
        nullable=False,
    ),
)


messages = sa.Table(
    'messages', metadata,

    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('body', sa.Text, nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=func.now()),

    # ForeignKey
    sa.Column(
        'who_like',
        postgresql.ARRAY(sa.Integer),
        server_default='{}',
    ),
    sa.Column(
        'owner_id',
        sa.Integer,
        sa.ForeignKey(users.c.id, ondelete='CASCADE'),
        nullable=False,
    ),
    sa.Column(
        'room_id',
        sa.Integer,
        sa.ForeignKey(rooms.c.id, ondelete='CASCADE'),
        nullable=False,
    ),
)
