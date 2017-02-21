from sqlalchemy import Column, DateTime

from common.utils.date_ops import DateTimeOperations as DtOps
from flask_init import db


class BaseModel(db.Model):
    """
    Base model to be inherited across the project
    """
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: DtOps.ist_now())
    modified_at = Column(DateTime, default=lambda: DtOps.ist_now(), onupdate=lambda: DtOps.ist_now())
