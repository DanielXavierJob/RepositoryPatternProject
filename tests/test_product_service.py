import unittest
from unittest.mock import MagicMock

from sqlalchemy.exc import IntegrityError

from modules.products.product import Product
from modules.products.product_model import ProductUpdate
from modules.products.product_service import ProductService
from modules.stores.store import Store


class TestProductService(unittest.TestCase):

    def setUp(self):
        self.product_service = ProductService()
        self.mock_product_repository = MagicMock()
        self.mock_store_service = MagicMock()
        self.product_service.product_repository = self.mock_product_repository
        self.product_service.store_service = self.mock_store_service

    def test_get_all_success(self):
        # Arrange
        id_store = 1
        expected_products = [Product(id=1, name="Product1", unity_value=10, quantity=50),
                             Product(id=2, name="Product2", unity_value=20, quantity=30)]
        self.mock_product_repository.get_all.return_value = expected_products

        # Act
        response = self.product_service.get_all(id_store)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(len(response['data']), 2)

    def test_get_all_failure(self):
        # Arrange
        id_store = 1
        self.mock_product_repository.get_all.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.product_service.get_all(id_store)

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred where trying to get all products")

    def test_get_by_id_success(self):
        # Arrange
        id_store = 1
        product_id = 1
        expected_product = Product(id=product_id, name="Product1", unity_value=10, quantity=50)
        self.mock_product_repository.get_by_id.return_value = expected_product

        # Act
        response = self.product_service.get_by_id(id_store, product_id)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data']['id'], product_id)

    def test_get_by_id_not_found(self):
        # Arrange
        id_store = 1
        product_id = 999  # Assuming this ID doesn't exist
        self.mock_product_repository.get_by_id.return_value = None

        # Act
        response = self.product_service.get_by_id(id_store, product_id)

        # Assert
        self.assertEqual(response['status'], 404)
        self.assertEqual(response['message'], "Product not has been searched")

    def test_get_by_id_failure(self):
        # Arrange
        id_store = 1
        product_id = 1
        self.mock_product_repository.get_by_id.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.product_service.get_by_id(id_store, product_id)

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred where trying to get product by id")

    def test_create_success(self):
        # Arrange
        product_data = Product(id_store=1, name="Product", unity_value=50, quantity=10)
        store = Store(id=1, name="Store", opened=True)
        expected_product = Product(id=1, id_store=1, name="Product", unity_value=50, quantity=10)

        self.mock_store_service.get_by_id.return_value = {"status": 200, "message": "Store has been searched", "data": store}
        self.mock_product_repository.create.return_value = expected_product

        # Act
        response = self.product_service.create(product_data)

        # Assert
        self.assertEqual(response['status'], 201)
        self.assertEqual(response['data']['id'], 1)
        self.assertEqual(response['data']['id_store'], 1)
        self.assertEqual(response['data']['name'], "Product")
        self.assertEqual(response['data']['unity_value'], 50)
        self.assertEqual(response['data']['quantity'], 10)

    def test_create_store_not_found(self):
        # Arrange
        product_data = Product(id_store=1, name="Product", unity_value=50, quantity=10)

        self.mock_store_service.get_by_id.return_value = {"status": 404}

        # Act
        response = self.product_service.create(product_data)

        # Assert
        self.assertEqual(response['status'], 404)


    def test_update_success(self):
        # Arrange
        product_id = 1
        product_data = ProductUpdate(name="New Product", unity_value=60, quantity=20, id_store=2)
        existing_product = Product(id=product_id, id_store=1, name="Product", unity_value=50, quantity=10)

        self.mock_product_repository.get_by_id.return_value = existing_product
        self.mock_store_service.get_by_id.return_value = {"status": 200,
                                                          "data": Store(id=2, name="New Store", opened=True)}

        # Act
        response = self.product_service.update(1, product_id, product_data)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data']['id'], product_id)
        self.assertEqual(response['data']['id_store'], 2)
        self.assertEqual(response['data']['name'], "New Product")
        self.assertEqual(response['data']['unity_value'], 60)
        self.assertEqual(response['data']['quantity'], 20)


    def test_update_failure(self):
        # Arrange
        product_id = 1
        update_data = ProductUpdate(name="Updated Product", unity_value=75, quantity=20, id_store=1)
        existing_product = Product(id=product_id, id_store=1, name="Product", unity_value=50, quantity=10)
        self.mock_product_repository.get_by_id.return_value = existing_product
        self.mock_store_service.get_by_id.return_value = {"status": 500}  # Simulate store not found
        self.mock_product_repository.update.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.product_service.update(1, product_id, update_data)

        # Assert
        self.assertEqual(response['status'], 500)

    def test_remove_success(self):
        # Arrange
        product_id = 1
        existing_product = Product(id=product_id, id_store=1, name="Product", unity_value=50, quantity=10)
        self.mock_product_repository.get_by_id.return_value = {"status": 200, "data": existing_product}

        # Act
        response = self.product_service.remove(1, product_id)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['message'], "Product removed successfully")


    def test_remove_failure(self):
        # Arrange
        product_id = 1
        existing_product = Product(id=product_id, id_store=1, name="Product", unity_value=50, quantity=10)
        self.mock_product_repository.get_by_id.return_value = {"status": 200, "data": existing_product}
        self.mock_product_repository.remove.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.product_service.remove(1, product_id)

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred where trying delete a existing product")
