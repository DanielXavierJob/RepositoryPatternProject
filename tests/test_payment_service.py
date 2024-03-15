import unittest
from unittest.mock import MagicMock

from modules.clients.client import Client
from modules.payments.payment_model import PaymentCreate
from modules.payments.payment_service import PaymentService
from modules.payments.payment import Payment
from sqlalchemy.exc import IntegrityError

from modules.products.product import Product
from modules.stores.store import Store


class TestPaymentService(unittest.TestCase):

    def setUp(self):
        self.payment_service = PaymentService()
        self.mock_payment_repository = MagicMock()
        self.mock_client_service = MagicMock()
        self.mock_product_service = MagicMock()
        self.mock_store_service = MagicMock()

        self.payment_service.payment_repository = self.mock_payment_repository
        self.payment_service.client_service = self.mock_client_service
        self.payment_service.product_service = self.mock_product_service
        self.payment_service.store_service = self.mock_store_service

    def test_get_all_success(self):
        # Arrange
        expected_payments = [Payment(id=1, id_client=1, id_product=1, quantity=2, unity_value=50, total_value=100),
                             Payment(id=2, id_client=2, id_product=2, quantity=1, unity_value=30, total_value=30)]
        self.mock_payment_repository.get_all.return_value = expected_payments

        # Act
        response = self.payment_service.get_all(id_client=1, id_product=1)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(len(response['data']), 2)

    def test_get_all_failure(self):
        # Arrange
        self.mock_payment_repository.get_all.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.payment_service.get_all(id_client=1, id_product=1)

        # Assert
        self.assertEqual(response['status'], 500)

    def test_get_by_id_success(self):
        # Arrange
        payment_id = 1
        expected_client = Client(id=1, name="John Doe", money=100)
        expected_product = Product(id=1, name="Product", unity_value=50)
        expected_payment = Payment(id=payment_id, id_client=1, id_product=1, quantity=2, unity_value=50,
                                   total_value=100, client=expected_client, product=expected_product)

        self.mock_payment_repository.get_by_id.return_value = expected_payment

        # Act
        response = self.payment_service.get_by_id(payment_id)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data']['id'], payment_id)

    def test_get_by_id_not_found(self):
        # Arrange
        payment_id = 999  # Assuming this ID doesn't exist
        self.mock_payment_repository.get_by_id.return_value = None

        # Act
        response = self.payment_service.get_by_id(payment_id)

        # Assert
        self.assertEqual(response['status'], 404)

    def test_get_by_id_failure(self):
        # Arrange
        payment_id = 1
        self.mock_payment_repository.get_by_id.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.payment_service.get_by_id(payment_id)

        # Assert
        self.assertEqual(response['status'], 500)

    def test_create_success(self):
        # Arrange
        payment_data = PaymentCreate(id_client=1, id_product=1, id_store=1, quantity=2)
        store = Store(id=1, name="Store", opened=True)
        product = Product(id=1, name="Product", unity_value=50)
        client = Client(id=1, name="John Doe", money=200)
        expected_payment = Payment(id=1, id_client=1,client=client, product=product, id_product=1, quantity=2, unity_value=50, total_value=100)

        self.mock_store_service.get_by_id.return_value = {"status": 200, "data": store}
        self.mock_product_service.get_by_id.return_value = {"status": 200, "data": product}
        self.mock_client_service.get_by_id.return_value = {"status": 200, "data": client}
        self.mock_payment_repository.create.return_value = expected_payment

        # Act
        response = self.payment_service.create(payment_data)

        # Assert
        self.assertEqual(response['status'], 201)
        self.assertEqual(response['data']['id'], 1)
        self.assertEqual(response['data']['id_client'], 1)
        self.assertEqual(response['data']['id_product'], 1)
        self.assertEqual(response['data']['quantity'], 2)
        self.assertEqual(response['data']['unity_value'], 50)
        self.assertEqual(response['data']['total_value'], 100)

    def test_create_store_closed(self):
        # Arrange
        payment_data = PaymentCreate(id_client=1, id_product=1, id_store=1, quantity=2)
        store = Store(id=1, name="Store", opened=False)

        self.mock_store_service.get_by_id.return_value = {"status": 200, "data": store}

        # Act
        response = self.payment_service.create(payment_data)

        # Assert
        self.assertEqual(response['status'], 403)
        self.assertEqual(response['message'], "Payment not has been created because store is closed")

    def test_create_product_not_found(self):
        # Arrange
        payment_data = PaymentCreate(id_client=1, id_product=1, id_store=1, quantity=2)
        store = Store(id=1, name="Store", opened=True)

        self.mock_store_service.get_by_id.return_value = {"status": 200, "data": store}
        self.mock_product_service.get_by_id.return_value = {"status": 404}

        # Act
        response = self.payment_service.create(payment_data)

        # Assert
        self.assertEqual(response['status'], 404)

if __name__ == '__main__':
    unittest.main()
