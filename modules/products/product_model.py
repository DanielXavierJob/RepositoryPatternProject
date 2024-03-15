# store_model.py

from typing import Optional
from flask_restx import fields
from pydantic import BaseModel
from modules.products.product import Product


class ProductCreate(BaseModel):
    name: str
    unity_value: float
    quantity: int
    id_store: int

    class Config:
        from_attributes = True

    @staticmethod
    def model_flask(bp):
        return bp.model("ProductCreate", {
            "name": fields.String(description="Nome do produto", required=True),
            "quantity": fields.Integer(description="Quantidade do produto", required=True),
            "unity_value": fields.Float(description="Valor do produto", required=True),
        })

    def to_orm_object(self):
        return Product(**self.dict())


class ProductUpdate(BaseModel):
    name: Optional[str]
    unity_value: Optional[float]
    quantity: Optional[int]
    id_store: Optional[int]

    class Config:
        from_attributes = True

    @staticmethod
    def model_flask(bp):
        return bp.model("ProductUpdate", {
            "name": fields.String(description="Novo nome do produto", required=False),
            "quantity": fields.Integer(description="Nova quantidade do produto", required=False),
            "unity_value": fields.Float(description="Novo valor do produto", required=False),
            "id_store": fields.Integer(description="Novo ID da loja", required=False)
        })
