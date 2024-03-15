import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import scoped_session, sessionmaker
from database.db import db_connection
from modules.stores.store_repository import StoreRepository
from modules.stores.store import Store


class TestStoreRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = scoped_session(sessionmaker())
        db_connection.session = cls.session

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def setUp(self):
        self.repository = StoreRepository()

    @patch('modules.stores.store_repository.db_connection.session')
    def test_get_all(self, mock_session):
        mock_session.query().filter().all.return_value = [Store(id=1, name='Store 1'), Store(id=2, name='Store 2')]
        stores = self.repository.get_all()
        self.assertEqual(len(stores), 2)

    @patch('modules.stores.store_repository.db_connection.session')
    def test_get_by_id(self, mock_session):
        mock_session.query().options().filter().first.return_value = Store(id=1, name='Store 1')
        store = self.repository.get_by_id(1)
        self.assertIsNotNone(store)
        self.assertEqual(store.id, 1)
        self.assertEqual(store.name, 'Store 1')

    @patch('modules.stores.store_repository.db_connection.session')
    def test_create(self, mock_session):
        new_store = Store(id=3, name='New Store')
        self.repository.create(new_store)
        mock_session.add.assert_called_once_with(new_store)
        mock_session.commit.assert_called_once()

    @patch('modules.stores.store_repository.db_connection.session')
    def test_update(self, mock_session):
        updated_store = Store(id=1, name='Updated Store')
        mock_session.query().get.return_value = updated_store
        self.repository.update(updated_store)
        mock_session.commit.assert_called_once()

    @patch('modules.stores.store_repository.db_connection.session')
    def test_remove(self, mock_session):
        # Mocking a store object
        store_to_delete = MagicMock()

        # Patching the session to return our mock session
        with patch('modules.stores.store_repository.db_connection.session', mock_session):
            # Creating an instance of StoreRepository
            store_repository = StoreRepository()

            # Calling the remove method
            store_repository.remove(store_to_delete)

        # Asserting that soft_delete was called once with store_to_delete
        store_to_delete.soft_delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()
