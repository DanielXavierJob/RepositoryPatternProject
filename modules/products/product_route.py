# product_routes.py

from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource
from modules.products.product_model import ProductUpdate, ProductCreate
from modules.products.product_service import ProductService

product_bp = Namespace(
    "products", description="APIs to product", path="/public/products"
)


@product_bp.route('/<int:id_store>')
class ProductsRoute(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_service = ProductService()

    def get(self, id_store: int):
        response = self.product_service.get_all(id_store)
        return make_response(jsonify(response), response.get('status', 200))

    @product_bp.expect(ProductCreate.model_flask(product_bp))
    def post(self, id_store: int):
        data = request.json
        product = ProductCreate(name=data.get('name'),
                                unity_value=data.get('unity_value', 0),
                                quantity=data.get('quantity', 0),
                                id_store=id_store)
        response = self.product_service.create(product.to_orm_object())
        return make_response(jsonify(response), response.get('status', 200))


@product_bp.route('/<int:id_store>/<int:id>')
class ProductsRouteByID(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_service = ProductService()

    def get(self, id_store:int, id: int):
        response = self.product_service.get_by_id(id_store, id)
        return make_response(jsonify(response), response.get('status', 200))

    @product_bp.expect(ProductUpdate.model_flask(product_bp))
    def put(self, id_store: int, id: int):
        data = request.json
        product = ProductUpdate(name=data.get('name', None),
                                unity_value=data.get('unity_value', None),
                                quantity=data.get('quantity', None),
                                id_store=data.get('id_store', None))
        response = self.product_service.update(id_store, id, product)
        return make_response(jsonify(response), response.get('status', 200))

    def delete(self, id_store: int, id: int):
        response = self.product_service.remove(id_store, id)
        return make_response(jsonify(response), response.get('status', 200))