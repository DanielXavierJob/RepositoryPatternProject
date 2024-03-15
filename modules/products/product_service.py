# store_service.py

from typing import Optional
from sqlalchemy.exc import IntegrityError
from modules.products.product import Product
from modules.products.product_model import ProductUpdate
from modules.products.product_repository import ProductRepository
from modules.stores.store_service import StoreService


class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        self.store_service = StoreService()

    def get_all(self, id_store: int):
        try:
            products = self.product_repository.get_all(id_store)

            return {"message": "Products has been searched", "data": [product.to_dict() for product in products],
                    "status": 200}
        except IntegrityError:
            return {"message": "A error occurred where trying to get all products", "data": None,  "status": 500}

    def get_by_id(self, id_store: int, id: int, returns_product: Optional[bool] = False):
        try:
            product = self.product_repository.get_by_id(id_store, id)
            if product:
                return {"message": "Product has been searched", "data": product.to_dict() if returns_product is False
                        else product, "status": 200}
            else:
                return {"message": "Product not has been searched", "data": None, "status": 404}
        except IntegrityError:
            return {"message": "A error occurred where trying to get product by id", "data": None, "status": 500}

    def create(self, data: Product):
        try:
            store = self.store_service.get_by_id(data.id_store, True)
            if store.get('status', 404) == 200:
                product = self.product_repository.create(data)
                return {"message": "Product has been created", "data": product.to_dict(), "status": 201}
            else:
                return store
        except IntegrityError as e:
            print(e)
            return {"message": "A error occurred where trying to add a new product", "data": None,  "status": 500}

    def update(self,id_store: int, id: int, data: ProductUpdate):
        try:
            product_by_id = self.get_by_id(id_store, id, True)
            if product_by_id.get('status', 404) == 200:

                product: Product = product_by_id.get('data')
                if data.name is not None:
                    product.name = data.name

                if data.unity_value is not None:
                    product.unity_value = data.unity_value

                if data.quantity is not None:
                    product.quantity = data.quantity

                if data.id_store is not None:
                    store = self.store_service.get_by_id(data.id_store, True)
                    if store.get('status', 404) == 200:
                        product.id_store = data.id_store
                    else:
                        return store

                self.product_repository.update(product)
                return {"message": "Product has been updated", "data": product.to_dict(), "status": 200}

            return product_by_id
        except IntegrityError:
            return {"message": "A error occurred", "data": None, "status": 500}

    def remove(self, id_store: int, id: int):
        try:
            product_by_id = self.get_by_id(id_store, id, True)
            if product_by_id.get('status', 404) == 200:
                product: Product = product_by_id.get('data')
                self.product_repository.remove(product)
                return {"message": "Product removed successfully", "data": None, "status": 200}

            return product_by_id
        except IntegrityError:
            return {"message": "A error occurred where trying delete a existing product", "data": None,
                    "status": 500}
