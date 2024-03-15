# store_repository.py

from typing import Optional

from sqlalchemy.orm import joinedload

from database.db import db_connection
from modules.stores.store import Store
from standard.repository import Repository


class StoreRepository(Repository):

    def get_all(self):
        stores = db_connection.session.query(Store).filter(Store.deleted_at == None).all()
        return stores

    def get_by_id(self, id: int, is_deleted: Optional[bool] = False):
        store = (db_connection.session.query(Store)
                 .options(joinedload(Store.products))
                 .filter(Store.deleted_at == None if is_deleted is False else None,
                         Store.id == id)
                 .first())
        return store

    def create(self, data: Store):
        db_connection.session.add(data)
        db_connection.session.commit()
        return data

    def update(self, store: Store):
        store.update()

    def remove(self, store: Store):
        store.soft_delete()


