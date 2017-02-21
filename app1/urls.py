from flask import Blueprint
from flask_restful import Api

from app1.views import CustomerAPI

# Primary blueprint route to be used for all APIs for app1
app1_bp = Blueprint('app1', __name__, url_prefix='/app1')
app1_api = Api()
app1_api.init_app(app1_bp)

app1_api.add_resource(CustomerAPI, '/customer/')
