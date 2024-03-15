# payment_repository.py

from typing import Optional
from database.db import db_connection
from modules.payments.payment import Payment
from standard.repository import Repository


class PaymentRepository(Repository):
    def get_all(self, id_client: Optional[int], id_product: Optional[int]):
        payments = db_connection.session.query(Payment).filter(Payment.deleted_at == None)

        if id_client is not None:
            payments = payments.filter(Payment.id_client == id_client)

        if id_product is not None:
            payments = payments.filter(Payment.id_product == id_product)

        payments = payments.all()
        return payments

    def get_by_id(self, id: int, is_deleted: Optional[bool] = False):
        payment = (db_connection.session.query(Payment)
                  .filter(Payment.deleted_at == None if is_deleted is False else None,
                          Payment.id == id)
                  .first())
        return payment

    def create(self, data: Payment):
        db_connection.session.add(data)
        db_connection.session.commit()
        return data

    def update(self, payment: Payment):
        payment.update()

    def remove(self, payment: Payment):
        payment.soft_delete()


