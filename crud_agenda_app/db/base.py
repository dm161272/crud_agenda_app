from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    """Prototype only. Switch to Alembic once the schema changes."""
    from crud_agenda_app.db import models  # noqa: F401  (registers tables)
    Base.metadata.create_all(engine)