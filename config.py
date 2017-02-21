import os

from common.utils import get_var

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEPLOYMENT_TYPE = 'BASE'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = get_var('SECRET_KEY', '<random_secret_key>')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Flask-Security settings
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('username', 'email')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = get_var('SECURITY_PASSWORD_SALT', '<random_password_salt>')
    SECURITY_DEFAULT_REMEMBER_ME = True
    SECURITY_REGISTERABLE = False

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_URL_PREFIX = '/admin'
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"

    # SQLAlchemy settings
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_SIZE = int(get_var('SQLALCHEMY_POOL_SIZE', 10))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Custom SQLAlchemy settings
    SQLALCHEMY_HOST = get_var('SQLALCHEMY_HOST', 'localhost')
    SQLALCHEMY_PORT = get_var('SQLALCHEMY_PORT', '5432')
    SQLALCHEMY_DATABASE = get_var('SQLALCHEMY_DATABASE', 'flask_dummy')
    SQLALCHEMY_USERNAME = get_var('SQLALCHEMY_USERNAME', 'flask_dummy_user')
    SQLALCHEMY_PASSWORD = get_var('SQLALCHEMY_PASSWORD', 'flask_dummy_pass')


class ProductionConfig(BaseConfig):
    DEPLOYMENT_TYPE = 'PRODUCTION'
    DEVELOPMENT = False
    DEBUG = False


class StagingConfig(BaseConfig):
    DEPLOYMENT_TYPE = 'STAGING'
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEPLOYMENT_TYPE = 'DEVELOPMENT'
    DEVELOPMENT = True
    DEBUG = True


env = get_var('DEPLOYMENT_TYPE', 'STAGING').upper()
if env == 'PRODUCTION':
    app_config = ProductionConfig
elif env == 'STAGING':
    app_config = StagingConfig
else:
    app_config = DevelopmentConfig
