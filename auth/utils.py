from getpass import getpass

from addict import Dict
from flask_security.utils import encrypt_password

from auth.models import User, Role
from flask_init import db


def add_user(roles=None):
    username = input('Enter username: ')
    assert User.query.filter_by(username=username).first() is None, 'User with this username already exists'

    email = input('Enter email address: ')
    if email:
        assert User.query.filter_by(email=email).first() is None, 'User with this email already exists'

    password = getpass('Enter password: ')
    assert password == getpass('Password (again):'), 'Passwords do not match'

    if roles is None:
        roles = input('Enter roles to be assigned (comma separated; leave blank if `None`): ')
        roles = roles.split(',')

    db_roles = Role.query.filter(Role.name.in_(roles)).all()
    password_hash = encrypt_password(password)
    user_data = Dict()
    user_data.email = email
    user_data.username = username
    user_data.password = password_hash
    user_data.active = True
    user_data.roles = db_roles

    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    print('User added.')
