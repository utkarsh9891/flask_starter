from sqlalchemy import Column, Integer, String, Boolean

from common.models import BaseModel


class Customer(BaseModel):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name
