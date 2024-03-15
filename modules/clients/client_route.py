# client_route.py

from flask import request, jsonify, make_response

from modules.clients.client_model import ClientCreate, ClientUpdate
from modules.clients.client_service import ClientService
from flask_restx import Namespace, Resource, fields

client_bp = Namespace(
    "clients", description="APIs to client", path="/public/clients"
)




@client_bp.route('')
class ClientsRoute(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_service = ClientService()

    def get(self):
        response = self.client_service.get_all()
        return make_response(jsonify(response), response.get('status', 200))

    @client_bp.expect(ClientCreate.model_flask(client_bp))
    def post(self):
        data = request.json
        client = ClientCreate(name=data.get('name'), money=data.get('money', 0))
        response = self.client_service.create(client.to_orm_object())
        return make_response(jsonify(response), response.get('status', 200))


@client_bp.route('/<int:id>')
class ClientsRouteByID(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_service = ClientService()

    def get(self, id: int):
        response = self.client_service.get_by_id(id)
        return make_response(jsonify(response), response.get('status', 200))

    @client_bp.expect(ClientUpdate.model_flask(client_bp))
    def put(self, id: int):
        data = request.json
        client = ClientUpdate(name=data.get('name', None), money=data.get('money', None))
        response = self.client_service.update(id, client)
        return make_response(jsonify(response), response.get('status', 200))

    def delete(self, id: int):
        response = self.client_service.remove(id)
        return make_response(jsonify(response), response.get('status', 200))