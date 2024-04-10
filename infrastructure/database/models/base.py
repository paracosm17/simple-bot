import datetime

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func


class Base(DeclarativeBase):
    pass


class CreatedMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
