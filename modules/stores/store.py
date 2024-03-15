# store.py

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from database.base_model import BaseModel


class Store(BaseModel):
    __tablename__ = 'stores'

    name = Column(String(255))
    opened = Column(Boolean, default=True)
    products = relationship("Product", back_populates="store")

    def __repr__(self):
        return f"<Store(name='{self.name}', opened={self.opened})>"

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "opened": self.opened,
                "products": [product.to_dict() for product in self.products],
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "deleted_at": self.deleted_at}
