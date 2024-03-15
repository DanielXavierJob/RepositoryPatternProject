# base_model.py
from sqlalchemy import Column, DateTime, INTEGER
from sqlalchemy.sql import func
from database.db import db_connection


class BaseModel(db_connection.Model):
    __abstract__ = True

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    def soft_delete(self):
        self.deleted_at = func.now()
        db_connection.session.add(self)
        db_connection.session.commit()

    def update(self):
        db_connection.session.add(self)
        db_connection.session.commit()