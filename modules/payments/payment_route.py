# payment_routes.py

from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, reqparse

from modules.payments.payment_model import PaymentCreate
from modules.payments.payment_service import PaymentService

payment_bp = Namespace(
    "payments", description="APIs to payments", path="/public/payments"
)
parser_get = reqparse.RequestParser()
parser_get.add_argument("id_client", help="ID client", type=int)
parser_get.add_argument("id_product", help="ID product", type=int)

parser_delete = reqparse.RequestParser()
parser_delete.add_argument("returns_money", help="Returns money to client", type=bool)


@payment_bp.route('')
class PaymentsRoute(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service = PaymentService()

    @payment_bp.expect(parser_get)
    def get(self):
        args = parser_get.parse_args()
        id_client = args['id_client']
        id_product = args['id_product']
        response = self.payment_service.get_all(id_client, id_product)
        return make_response(jsonify(response), response.get('status', 200))

    @payment_bp.expect(PaymentCreate.model_flask(payment_bp))
    def post(self):
        data = request.json
        payment = PaymentCreate(id_client=data.get('id_client', None),
                                id_product=data.get('id_product', None),
                                id_store=data.get('id_store', None),
                                quantity=data.get('quantity', 0))

        response = self.payment_service.create(payment)
        return make_response(jsonify(response), response.get('status', 200))


@payment_bp.route('/<int:id>')
class PaymentsRouteByID(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service = PaymentService()

    def get(self, id: int):
        response = self.payment_service.get_by_id(id)
        return make_response(jsonify(response), response.get('status', 200))

    @payment_bp.expect(parser_delete)
    def delete(self, id: int):
        args = parser_delete.parse_args()
        returns_money = args['returns_money']
        response = self.payment_service.remove(id, returns_money)
        return make_response(jsonify(response), response.get('status', 200))