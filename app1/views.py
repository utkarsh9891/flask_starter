from addict import Dict
from flask_restful import Resource

from app1.models import Customer
from app1.serializer import CustomerSchema
from common.utils.vars import success, failure


class CustomerAPI(Resource):
    def get(self):
        resp_dict = Dict()
        resp_status = failure

        customers = Customer.query.all()
        customer_schema = CustomerSchema().dump(customers, many=True)
        if customer_schema.errors:
            resp_dict.message = customer_schema.errors
        else:
            resp_dict.customers = customer_schema.data
            resp_status = success

        return resp_dict, resp_status
