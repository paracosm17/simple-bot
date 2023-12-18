from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tgbot.config import DbConfig
from infrastructure.database.models.base import Base


def create_engine(db: DbConfig, echo=False):
    engine = create_async_engine(
        db.construct_sqlite_url("database.db"),
        query_cache_size=1200,
        #pool_size=20,
        #max_overflow=200,
        future=True,
        echo=echo,
    )
    return engine


def create_session_pool(engine):
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool


def create_metadata():
    return Base.metadata.create_all
