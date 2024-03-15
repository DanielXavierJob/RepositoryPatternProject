import unittest
from modules.products.product_model import ProductCreate, ProductUpdate


class TestProductModel(unittest.TestCase):

    def test_product_create(self):
        data = {
            "name": "Product 1",
            "quantity": 10,
            "unity_value": 5.0,
            "id_store": 1
        }
        product_create = ProductCreate(**data)
        self.assertEqual(product_create.name, "Product 1")
        self.assertEqual(product_create.quantity, 10)
        self.assertEqual(product_create.unity_value, 5.0)
        self.assertEqual(product_create.id_store, 1)

    def test_product_update(self):
        data = {
            "name": "Updated Product",
            "quantity": 20,
            "unity_value": 10.0,
            "id_store": 2
        }
        product_update = ProductUpdate(**data)
        self.assertEqual(product_update.name, "Updated Product")
        self.assertEqual(product_update.quantity, 20)
        self.assertEqual(product_update.unity_value, 10.0)
        self.assertEqual(product_update.id_store, 2)


if __name__ == '__main__':
    unittest.main()
