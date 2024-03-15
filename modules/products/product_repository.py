# store_repository.py

from typing import Optional
from database.db import db_connection
from modules.products.product import Product
from standard.repository import Repository


class ProductRepository(Repository):

    def get_all(self, id_store: int):
        products = db_connection.session.query(Product).filter(Product.deleted_at == None,
                                                               Product.id_store == id_store).all()
        return products

    def get_by_id(self, id_store: int, id: int, is_deleted: Optional[bool] = False):
        product = (db_connection.session.query(Product)
                  .filter(Product.deleted_at == None if is_deleted is False else None,
                          Product.id == id,
                          Product.id_store == id_store)
                  .first())
        return product

    def create(self, data: Product):
        db_connection.session.add(data)
        db_connection.session.commit()
        return data

    def update(self, product: Product):
        product.update()

    def remove(self, product: Product):
        product.soft_delete()


