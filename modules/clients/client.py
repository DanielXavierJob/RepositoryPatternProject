# client.py
from typing import Optional

from flask_restx import fields
from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship

from database.base_model import BaseModel
from modules.payments.payment import Payment


class Client(BaseModel):
    __tablename__ = 'clients'

    name = Column(String(255))
    money = Column(Numeric(precision=10, scale=2))

    payments = relationship(Payment, back_populates="client")

    def __repr__(self):
        return f"<Client(name='{self.name}', money='{self.money}')>"

    def to_dict(self):
        return ({"id": self.id, "name": self.name, "money": self.money, "created_at": self.created_at, "updated_at":
                self.updated_at, "deleted_at": self.deleted_at})
