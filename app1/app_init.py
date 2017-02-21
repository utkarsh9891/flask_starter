from app1.admin import CustomerAdminView
from app1.models import Customer
from app1.urls import app1_bp


def init_app1(flask_app, admin, db):
    # Register Blueprints
    flask_app.register_blueprint(app1_bp)

    # Register admins
    admin.add_view(CustomerAdminView(Customer, db.session))
