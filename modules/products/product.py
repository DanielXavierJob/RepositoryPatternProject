# payment.py

from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base_model import BaseModel
from modules.stores.store import Store


class Product(BaseModel):
    __tablename__ = 'products'

    name = Column(String(255))
    unity_value = Column(Numeric(precision=10, scale=2))
    quantity = Column(Integer())
    id_store = Column(Integer, ForeignKey('stores.id'))
    store = relationship(Store, back_populates="products")

    payments = relationship("Payment", back_populates="product")

    def __repr__(self):
        return (f"<Product(name='{self.name}', unity_value={self.unity_value}, quantity={self.unity_value}, "
                f"id_store={self.id_store})>")

    def to_dict(self):
        return ({"id": self.id,
                 "name": self.name,
                 "unity_value": float(self.unity_value),
                 "quantity": self.quantity,
                 "id_store": self.id_store,
                 "created_at": self.created_at,
                 "updated_at": self.updated_at,
                 "deleted_at": self.deleted_at})
