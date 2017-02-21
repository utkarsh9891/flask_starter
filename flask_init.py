from flask import Flask, url_for
from flask_admin import Admin
from flask_admin import helpers
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

from common.forms import ExtendedLoginForm
from common.utils import get_var
from config import app_config

app = None
user_datastore = None
db = SQLAlchemy()
security = Security()
admin = Admin(name='FlaskDummy', base_template='master.html', template_mode='bootstrap3')


# Register blueprint(s) and admin(s)-- prevent circular imports
def init_apps(flask_app):
    from app1.app_init import init_app1
    from auth.app_init import init_auth
    admin.init_app(flask_app)
    init_app1(flask_app=flask_app, admin=admin, db=db)
    init_auth(flask_app=flask_app, admin=admin, db=db)


# Register security(s) -- prevent circular imports
def register_security(flask_app):
    global user_datastore
    from auth.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(flask_app, user_datastore, login_form=ExtendedLoginForm)

    # Source: https://github.com/flask-admin/Flask-Admin/tree/master/examples/auth
    # define a context processor for merging flask-admin's template context into the flask-security views.
    @flask_app.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
            get_url=url_for
        )


def create_app(package_name='flask_dummy'):
    """
    Returns a :class:`Flask` application instance configured with common
    functionality for the Flask Dummy platform.
    :param package_name: application package name
    :return: the flask app
    """
    global app
    app = Flask(package_name, instance_relative_config=True)

    # Configurations
    if get_var('APP_CONFIG', ''):
        # this can be used to define custom configuration
        app.config.from_object(get_var('APP_CONFIG'))
    else:
        app.config.from_object(app_config)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{host}:{port}/{database}'.format(
        username=app.config.get('SQLALCHEMY_USERNAME', ''),
        password=app.config.get('SQLALCHEMY_PASSWORD', ''),
        host=app.config.get('SQLALCHEMY_HOST', 'localhost'),
        port=app.config.get('SQLALCHEMY_PORT', 5432),
        database=app.config.get('SQLALCHEMY_DATABASE', 'flask_dummy')
    )

    db.init_app(app)
    init_apps(flask_app=app)
    register_security(app)

    return app
