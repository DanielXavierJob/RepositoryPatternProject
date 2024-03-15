# payment_model.py

from flask_restx import fields
from pydantic import BaseModel


class PaymentCreate(BaseModel):
    id_client: int
    id_product: int
    id_store: int
    quantity: int

    class Config:
        from_attributes = True

    @staticmethod
    def model_flask(bp):
        return bp.model("PaymentCreate", {
            "id_client": fields.Integer(description="ID do cliente", required=True),
            "id_product": fields.Integer(description="ID do produto", required=True),
            "id_store": fields.Integer(description="ID da loja", required=True),
            "quantity": fields.Integer(description="Quantidade do produto", required=True)
        })
