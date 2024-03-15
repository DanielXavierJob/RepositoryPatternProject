import unittest
from modules.products.product import Product


class TestProduct(unittest.TestCase):

    def test_product_attributes(self):
        product = Product(name='Test Product', unity_value=10.0, quantity=100, id_store=1)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.unity_value, 10.0)
        self.assertEqual(product.quantity, 100)
        self.assertEqual(product.id_store, 1)

    def test_to_dict(self):
        product = Product(name='Test Product', unity_value=10.0, quantity=100, id_store=1)
        product_dict = product.to_dict()
        self.assertEqual(product_dict['name'], 'Test Product')
        self.assertEqual(product_dict['unity_value'], 10.0)
        self.assertEqual(product_dict['quantity'], 100)
        self.assertEqual(product_dict['id_store'], 1)


if __name__ == '__main__':
    unittest.main()
