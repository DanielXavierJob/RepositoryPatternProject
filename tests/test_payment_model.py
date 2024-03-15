import unittest
from modules.payments.payment_model import PaymentCreate


class TestPaymentModel(unittest.TestCase):

    def test_payment_create(self):
        data = {
            "id_client": 1,
            "id_product": 2,
            "id_store": 3,
            "quantity": 10
        }
        payment_create = PaymentCreate(**data)
        self.assertEqual(payment_create.id_client, 1)
        self.assertEqual(payment_create.id_product, 2)
        self.assertEqual(payment_create.id_store, 3)
        self.assertEqual(payment_create.quantity, 10)


if __name__ == '__main__':
    unittest.main()
