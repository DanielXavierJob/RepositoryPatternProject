# client_repository.py
from typing import Optional

from database.db import db_connection
from modules.clients.client import Client
from modules.clients.client_model import ClientCreate
from standard.repository import Repository


class ClientRepository(Repository):

    def get_all(self):
        clients = db_connection.session.query(Client).filter(Client.deleted_at == None).all()
        return clients

    def get_by_id(self, id: int, is_deleted: Optional[bool] = False):
        client = db_connection.session.query(Client).filter(Client.deleted_at == None if is_deleted is False else None, Client.id
                                                            == id).first()
        return client

    def create(self, data: Client):
        db_connection.session.add(data)
        db_connection.session.commit()
        return data

    def update(self, client: Client):
        client.update()

    def remove(self, client: Client):
        client.soft_delete()


