# client_model.py

from typing import Optional
from flask_restx import fields
from pydantic import BaseModel

from modules.clients.client import Client


class ClientCreate(BaseModel):
    name: str
    money: float

    class Config:
        from_attributes = True

    @staticmethod
    def model_flask(bp):
        return bp.model("ClientCreate", {
            "name": fields.String(description="Nome do cliente", required=True),
            "money": fields.Float(description="Dinheiro do cliente", required=False)
        })

    def to_orm_object(self):
        return Client(**self.dict())


class ClientUpdate(BaseModel):
    name: Optional[str]
    money: Optional[float]

    class Config:
        from_attributes = True

    @staticmethod
    def model_flask(bp):
        return bp.model("ClientUpdate", {
            "name": fields.String(description="Novo nome do cliente", required=False),
            "money": fields.Float(description="Novo dinheiro do cliente", required=False)
        })