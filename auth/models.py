from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import backref, relationship

from common.models import BaseModel


class Role(BaseModel, RoleMixin):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    active = Column(Boolean)
    first_name = Column(String(60))
    last_name = Column(String(60))

    roles = relationship('Role', secondary='user_roles', backref=backref('users', lazy='dynamic'))

    def __str__(self):
        if self.first_name:
            return ' '.join(filter(None, [self.first_name, self.last_name]))
        else:
            return self.username

    @property
    def name(self):
        if self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.first_name


class UserRoles(BaseModel):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('role.id', ondelete='CASCADE'))
