# client_service.py

from typing import Optional
from sqlalchemy.exc import IntegrityError
from modules.clients.client import Client
from modules.clients.client_model import ClientUpdate
from modules.clients.client_repository import ClientRepository


class ClientService:
    def __init__(self):
        self.client_repository = ClientRepository()

    def get_all(self):
        try:
            clients = self.client_repository.get_all()
            return {"message": "Clients has been searched", "data": [client.to_dict() for client in clients], "status":
                    200}
        except IntegrityError:
            return {"message": "A error occurred where trying to get all client", "data": None,  "status": 500}

    def get_by_id(self, id: int, returns_client: Optional[bool] = False):
        try:
            client = self.client_repository.get_by_id(id)
            if client:
                return {"message": "Client has been searched", "data": client.to_dict() if returns_client is False else
                        client, "status": 200}
            else:
                return {"message": "Client not has been searched", "data": None, "status": 404}
        except IntegrityError:
            return {"message": "A error occurred where trying to get client by id", "data": None, "status": 500}

    def create(self, data: Client):
        try:
            client = self.client_repository.create(data)
            return {"message": "Client has been created", "data": client.to_dict(), "status": 201}
        except IntegrityError as e:
            print(e)
            return {"message": "A error occurred where trying to add a new client", "data": None,  "status": 500}

    def update(self, id: int, data: ClientUpdate):
        try:
            client_by_id = self.get_by_id(id, True)
            if client_by_id.get('status', 404) == 200:

                client: Client = client_by_id.get('data')
                if data.name is not None:
                    client.name = data.name

                if data.money is not None:
                    client.money = data.money

                self.client_repository.update(client)
                return {"message": "Client has been updated", "data": client.to_dict(), "status": 200}

            return client_by_id
        except IntegrityError:
            return {"message": "A error occurred", "data": None, "status": 500}

    def remove(self, id: int):
        try:
            client_by_id = self.get_by_id(id, True)
            if client_by_id.get('status', 404) == 200:
                client: Client = client_by_id.get('data')
                self.client_repository.remove(client)
                return {"message": "Cliente removed successfully", "data": None, "status": 200}

            return client_by_id
        except IntegrityError:
            return {"message": "A error occurred where trying delete a existing client", "data": None,
                    "status": 500}
