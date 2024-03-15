# store_model.py

from typing import Optional
from flask_restx import fields
from pydantic import BaseModel

from modules.stores.store import Store


class StoreCreate(BaseModel):
    name: str
    opened: bool

    class Config:
        from_attributes = True

    @staticmethod
    def model_flask(bp):
        return bp.model("StoreCreate", {
            "name": fields.String(description="Nome da loja", required=True),
            "opened": fields.Float(description="Loja aberta/fechada", required=False),
        })

    def to_orm_object(self):
        return Store(**self.dict())


class StoreUpdate(BaseModel):
    name: Optional[str]
    opened: Optional[bool]

    class Config:
        from_attributes = True

    @staticmethod
    def model_flask(bp):
        return bp.model("StoreUpdate", {
            "name": fields.String(description="Nome da loja", required=False),
            "opened": fields.Float(description="Loja aberta/fechada", required=False),
        })
