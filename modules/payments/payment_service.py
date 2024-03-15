# payment_service.py

from typing import Optional
from sqlalchemy.exc import IntegrityError

from modules.clients.client import Client
from modules.clients.client_service import ClientService
from modules.payments.payment import Payment
from modules.payments.payment_model import PaymentCreate
from modules.payments.payment_repository import PaymentRepository
from modules.products.product import Product
from modules.products.product_service import ProductService
from modules.stores.store import Store
from modules.stores.store_service import StoreService


class PaymentService:
    def __init__(self):
        self.payment_repository = PaymentRepository()
        self.client_service = ClientService()
        self.store_service = StoreService()
        self.product_service = ProductService()

    def get_all(self, id_client: Optional[int], id_product: Optional[int]):
        try:
            if id_client is None and id_product is None:
                return {"message": "id_client or id_product is required to get payments", "data": None, "status": 403}
            payments = self.payment_repository.get_all(id_client=id_client, id_product=id_product)

            return {"message": "Payments has been searched", "data": [payment.to_dict(expand_relations=False) for payment in payments],
                    "status": 200}
        except IntegrityError:
            return {"message": "A error occurred where trying to get all payments", "data": None,  "status": 500}

    def get_by_id(self, id: int, returns_payment: Optional[bool] = False):
        try:
            payment = self.payment_repository.get_by_id(id)
            if payment:
                return {"message": "Payment has been searched", "data": payment.to_dict() if returns_payment is False
                        else payment, "status": 200}
            else:
                return {"message": "Payment not has been searched", "data": None, "status": 404}
        except IntegrityError:
            return {"message": "A error occurred where trying to get payment by id", "data": None, "status": 500}

    def create(self, data: PaymentCreate):
        try:
            store = self.store_service.get_by_id(data.id_store, True)
            if store.get('status', 404) == 404:
                return store
            store: Store = store.get('data')

            if store.opened is False:
                return {"message": "Payment not has been created because store is closed",
                        "data": None, "status": 403}

            product = self.product_service.get_by_id(data.id_store, data.id_product, True)
            if product.get('status', 404) == 404:
                return product
            product: Product = product.get('data')

            client = self.client_service.get_by_id(data.id_client, True)
            if client.get('status', 404) == 404:
                return client
            client: Client = client.get('data')

            # Check if value of money client contains value to subtract
            value_product_total = product.unity_value * data.quantity

            if client.money < value_product_total:
                return {"message": "Payment not has been created because money of client is less than value of product",
                        "data": None, "status": 403}

            client.money -= value_product_total
            self.client_service.update(client.id, client)

            payment_data = Payment(id_client=data.id_client,
                                   id_product=data.id_product,
                                   quantity=data.quantity,
                                   unity_value=product.unity_value,
                                   total_value=value_product_total)

            payment = self.payment_repository.create(payment_data)
            return {"message": "Payment has been created", "data": payment.to_dict(), "status": 201}
        except IntegrityError as e:
            print(e)
            return {"message": "A error occurred where trying to add a new payment", "data": None,  "status": 500}

    def remove(self, id: int, returns_money: Optional[bool] = False):
        try:
            payment_by_id = self.get_by_id(id, True)
            if payment_by_id.get('status', 404) == 200:
                payment: Payment = payment_by_id.get('data')

                if returns_money:
                    payment.client.money += payment.total_value
                    self.client_service.update(payment.client.id, payment.client)

                self.payment_repository.remove(payment)
                return {"message": f"Payment removed successfully"
                                   f"{f', returned {payment.total_value} to client' if returns_money is True else ''}",
                        "data": None, "status": 200}

            return payment_by_id
        except IntegrityError:
            return {"message": "A error occurred where trying delete a existing payment", "data": None,
                    "status": 500}
