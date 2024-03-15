import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import scoped_session, sessionmaker
from database.db import db_connection
from modules.products.product_repository import ProductRepository
from modules.products.product import Product


class TestProductRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = scoped_session(sessionmaker())
        db_connection.session = cls.session

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def setUp(self):
        self.repository = ProductRepository()

    @patch('modules.products.product_repository.db_connection.session')
    def test_get_all(self, mock_session):
        mock_session.query().filter().all.return_value = [
            Product(id=1, name='Product 1', id_store=1),
            Product(id=2, name='Product 2', id_store=1)
        ]
        products = self.repository.get_all(id_store=1)
        self.assertEqual(len(products), 2)

    @patch('modules.products.product_repository.db_connection.session')
    def test_get_by_id(self, mock_session):
        mock_session.query().filter().first.return_value = Product(id=1, name='Product 1', id_store=1)
        product = self.repository.get_by_id(id_store=1, id=1)
        self.assertIsNotNone(product)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, 'Product 1')

    @patch('modules.products.product_repository.db_connection.session')
    def test_create(self, mock_session):
        new_product = Product(id=3, name='New Product', id_store=1)
        self.repository.create(new_product)
        mock_session.add.assert_called_once_with(new_product)
        mock_session.commit.assert_called_once()

    @patch('modules.products.product_repository.db_connection.session')
    def test_update(self, mock_session):
        updated_product = Product(id=1, name='Updated Product', id_store=1)
        mock_session.query().get.return_value = updated_product
        self.repository.update(updated_product)
        mock_session.commit.assert_called_once()

    @patch('modules.products.product_repository.db_connection.session')
    def test_remove(self, mock_session):
        # Mocking a product object
        product_to_delete = MagicMock()

        # Patching the session to return our mock session
        with patch('modules.products.product_repository.db_connection.session', mock_session):
            # Creating an instance of ProductRepository
            product_repository = ProductRepository()

            # Calling the remove method
            product_repository.remove(product_to_delete)

        # Asserting that soft_delete was called once with product_to_delete
        product_to_delete.soft_delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()
