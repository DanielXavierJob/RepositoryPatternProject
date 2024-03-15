import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import scoped_session, sessionmaker
from database.db import db_connection
from modules.payments.payment_repository import PaymentRepository
from modules.payments.payment import Payment


class TestPaymentRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = scoped_session(sessionmaker())
        db_connection.session = cls.session

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def setUp(self):
        self.repository = PaymentRepository()

    @patch('modules.payments.payment_repository.db_connection.session')
    def test_get_all(self, mock_session):
        mock_session.query().filter().all.return_value = [
            Payment(id=1, id_client=1, id_product=1),
            Payment(id=2, id_client=2, id_product=1)
        ]
        payments = self.repository.get_all(id_client=None, id_product=None)
        self.assertEqual(len(payments), 2)

    @patch('modules.payments.payment_repository.db_connection.session')
    def test_get_by_id(self, mock_session):
        mock_session.query().filter().first.return_value = Payment(id=1, id_client=1, id_product=1)
        payment = self.repository.get_by_id(id=1)
        self.assertIsNotNone(payment)
        self.assertEqual(payment.id, 1)
        self.assertEqual(payment.id_client, 1)
        self.assertEqual(payment.id_product, 1)

    @patch('modules.payments.payment_repository.db_connection.session')
    def test_create(self, mock_session):
        new_payment = Payment(id=3, id_client=1, id_product=1)
        self.repository.create(new_payment)
        mock_session.add.assert_called_once_with(new_payment)
        mock_session.commit.assert_called_once()

    @patch('modules.payments.payment_repository.db_connection.session')
    def test_update(self, mock_session):
        updated_payment = Payment(id=1, id_client=1, id_product=1)
        mock_session.query().get.return_value = updated_payment
        self.repository.update(updated_payment)
        mock_session.commit.assert_called_once()

    @patch('modules.payments.payment_repository.db_connection.session')
    def test_remove(self, mock_session):
        # Mocking a payment object
        payment_to_delete = MagicMock()

        # Patching the session to return our mock session
        with patch('modules.payments.payment_repository.db_connection.session', mock_session):
            # Creating an instance of PaymentRepository
            payment_repository = PaymentRepository()

            # Calling the remove method
            payment_repository.remove(payment_to_delete)

        # Asserting that soft_delete was called once with payment_to_delete
        payment_to_delete.soft_delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()
