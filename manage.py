import os
import sys
from getpass import getpass

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_security.utils import encrypt_password

from auth.utils import add_user
from flask_init import create_app, db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = create_app()
migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=8000))

manager.add_command("migrate", MigrateCommand)


@manager.command
def getpasswordhash():
    password = getpass()
    assert password == getpass('Password (again):'), 'Passwords do not match'

    password_hash = encrypt_password(password)
    print('Please find the encrypted password below\n', password_hash)


@manager.command
def createuser():
    add_user()


@manager.command
def createsuperuser():
    add_user(['superuser'])


if __name__ == "__main__":
    manager.run()
