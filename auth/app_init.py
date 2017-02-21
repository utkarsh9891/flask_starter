from auth.admin import UserAdminView, RoleAdminView
from auth.models import User, Role


def init_auth(flask_app, admin, db):
    # Register admins
    admin.add_view(UserAdminView(User, db.session, category='Authorization'))
    admin.add_view(RoleAdminView(Role, db.session, category='Authorization'))
