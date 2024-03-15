# store_service.py

from typing import Optional
from sqlalchemy.exc import IntegrityError
from modules.stores.store import Store
from modules.stores.store_model import StoreUpdate
from modules.stores.store_repository import StoreRepository


class StoreService:
    def __init__(self):
        self.store_repository = StoreRepository()

    def get_all(self):
        try:
            stores = self.store_repository.get_all()

            return {"message": "Stores has been searched", "data": [store.to_dict() for store in stores],
                    "status": 200}
        except IntegrityError:
            return {"message": "A error occurred where trying to get all stores", "data": None,  "status": 500}

    def get_by_id(self, id: int, returns_store: Optional[bool] = False):
        try:
            store = self.store_repository.get_by_id(id)
            if store:
                return {"message": "Store has been searched", "data": store.to_dict() if returns_store is False
                        else store, "status": 200}
            else:
                return {"message": "Store not has been searched", "data": None, "status": 404}
        except IntegrityError:
            return {"message": "A error occurred where trying to get store by id", "data": None, "status": 500}

    def create(self, data: Store):
        try:
            store = self.store_repository.create(data)
            return {"message": "Store has been created", "data": store.to_dict(), "status": 201}
        except IntegrityError as e:
            print(e)
            return {"message": "A error occurred where trying to add a new store", "data": None,  "status": 500}

    def update(self, id: int, data: StoreUpdate):
        try:
            store_by_id = self.get_by_id(id, True)
            if store_by_id.get('status', 404) == 200:

                store: Store = store_by_id.get('data')

                if data.name is not None:
                    store.name = data.name

                if data.opened is not None:
                    store.opened = data.opened

                self.store_repository.update(store)
                return {"message": "Store has been updated", "data": store.to_dict(), "status": 200}

            return store_by_id
        except IntegrityError:
            return {"message": "A error occurred", "data": None, "status": 500}

    def remove(self, id: int):
        try:
            store_by_id = self.get_by_id(id, True)
            if store_by_id.get('status', 404) == 200:
                store: Store = store_by_id.get('data')
                for product in store.products:
                    product.soft_delete()

                self.store_repository.remove(store)

                return {"message": f"Store removed successfully, with {len(store.products)} products deletions", "data": None, "status": 200}

            return store_by_id
        except IntegrityError:
            return {"message": "A error occurred where trying delete a existing store", "data": None,
                    "status": 500}
