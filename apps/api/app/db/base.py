from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so Alembic can discover them.
from app.db.models import *  # noqa: E402,F401,F403
