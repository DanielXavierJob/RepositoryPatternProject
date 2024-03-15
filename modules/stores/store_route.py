# store_route.py

from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource

from modules.stores.store_model import StoreCreate, StoreUpdate
from modules.stores.store_service import StoreService

store_bp = Namespace(
    "stores", description="APIs to store", path="/public/store"
)


@store_bp.route('')
class StoreRoute(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store_service = StoreService()

    def get(self):
        response = self.store_service.get_all()
        return make_response(jsonify(response), response.get('status', 200))

    @store_bp.expect(StoreCreate.model_flask(store_bp))
    def post(self):
        data = request.json
        store = StoreCreate(name=data.get('name'),
                            opened=data.get('opened', False))
        response = self.store_service.create(store.to_orm_object())
        return make_response(jsonify(response), response.get('status', 200))


@store_bp.route('/<int:id>')
class StoreRouteByID(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store_service = StoreService()

    def get(self, id: int):
        response = self.store_service.get_by_id(id)
        return make_response(jsonify(response), response.get('status', 200))

    @store_bp.expect(StoreUpdate.model_flask(store_bp))
    def put(self, id: int):
        data = request.json
        store = StoreUpdate(name=data.get('name', None),
                              opened=data.get('opened', None))
        response = self.store_service.update(id, store)
        return make_response(jsonify(response), response.get('status', 200))

    def delete(self, id: int):
        response = self.store_service.remove(id)
        return make_response(jsonify(response), response.get('status', 200))