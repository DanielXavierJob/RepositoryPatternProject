# payment.py
from typing import Optional

from sqlalchemy import Column,  Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base_model import BaseModel
from modules.products.product import Product


class Payment(BaseModel):
    __tablename__ = 'payments'

    id_client = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="payments")

    id_product = Column(Integer, ForeignKey('products.id'))
    product = relationship(Product, back_populates="payments")

    unity_value = Column(Numeric(precision=10, scale=2))
    quantity = Column(Integer())

    total_value = Column(Numeric(precision=10, scale=2))

    def __repr__(self):
        return (f"<Payment(id_client='{self.id_client}', id_product={self.id_product}, unity_value={self.unity_value}, "
                f"quantity={self.quantity}, total_value={self.total_value}>")

    def to_dict(self, expand_relations: Optional[bool] = True):
        data_dict = ({
                     "id": self.id,
                     "id_client": self.id_client,
                     "id_product": self.id_product,
                     "unity_value": float(self.unity_value),
                     "quantity": self.quantity,
                     "total_value": float(self.total_value),
                     "created_at": self.created_at,
                     "updated_at": self.updated_at,
                     "deleted_at": self.deleted_at
                     })

        if expand_relations:
            data_dict["client"] = self.client.to_dict()
            data_dict["product"] = self.product.to_dict()

        return data_dict
