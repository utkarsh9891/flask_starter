from marshmallow_sqlalchemy import ModelSchema

from app1.models import Customer
from flask_init import db


class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
        load_only = ['created_at', 'modified_at']
        sqla_session = db.session
