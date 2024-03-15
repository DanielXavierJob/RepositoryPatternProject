import unittest
from modules.payments.payment import Payment
from modules.clients.client import Client
from modules.products.product import Product


class TestPayment(unittest.TestCase):

    def test_payment_attributes(self):
        client = Client(id=1, name='Test Client', money=100.0)
        product = Product(id=1, name='Test Product', unity_value=10.0, quantity=100, id_store=1)
        payment = Payment(id_client=client.id, client=client, id_product=product.id, product=product,
                          unity_value=10.0, quantity=5, total_value=50.0)
        self.assertEqual(payment.id_client, client.id)
        self.assertEqual(payment.client, client)
        self.assertEqual(payment.id_product, product.id)
        self.assertEqual(payment.product, product)
        self.assertEqual(payment.unity_value, 10.0)
        self.assertEqual(payment.quantity, 5)
        self.assertEqual(payment.total_value, 50.0)

    def test_to_dict(self):
        client = Client(id=1, name='Test Client', money=100.0)
        product = Product(id=1, name='Test Product', unity_value=10.0, quantity=100, id_store=1)
        payment = Payment(id_client=client.id, client=client, id_product=product.id, product=product,
                          unity_value=10.0, quantity=5, total_value=50.0)
        payment_dict = payment.to_dict(expand_relations=False)
        self.assertEqual(payment_dict['id_client'], client.id)
        self.assertEqual(payment_dict['id_product'], product.id)
        self.assertEqual(payment_dict['unity_value'], 10.0)
        self.assertEqual(payment_dict['quantity'], 5)
        self.assertEqual(payment_dict['total_value'], 50.0)

        # Test expand_relations=True
        payment_dict_expanded = payment.to_dict(expand_relations=True)
        self.assertIn('client', payment_dict_expanded)
        self.assertIn('product', payment_dict_expanded)


if __name__ == '__main__':
    unittest.main()
