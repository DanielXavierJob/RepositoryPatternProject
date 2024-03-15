import unittest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from modules.stores.store_service import StoreService, StoreUpdate, Store

class TestStoreService(unittest.TestCase):

    def setUp(self):
        self.store_service = StoreService()
        self.mock_store_repository = MagicMock()
        self.store_service.store_repository = self.mock_store_repository

    def test_get_all_success(self):
        # Arrange
        expected_stores = [Store(id=1, name="Store1"), Store(id=2, name="Store2")]
        self.mock_store_repository.get_all.return_value = expected_stores

        # Act
        response = self.store_service.get_all()

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(len(response['data']), 2)

    def test_get_all_failure(self):
        # Arrange
        self.mock_store_repository.get_all.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.store_service.get_all()

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred where trying to get all stores")

    def test_get_by_id_success(self):
        # Arrange
        store_id = 1
        expected_store = Store(id=store_id, name="Store1")
        self.mock_store_repository.get_by_id.return_value = expected_store

        # Act
        response = self.store_service.get_by_id(store_id)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data']['id'], store_id)

    def test_get_by_id_not_found(self):
        # Arrange
        store_id = 999  # Assuming this ID doesn't exist
        self.mock_store_repository.get_by_id.return_value = None

        # Act
        response = self.store_service.get_by_id(store_id)

        # Assert
        self.assertEqual(response['status'], 404)
        self.assertEqual(response['message'], "Store not has been searched")

    def test_get_by_id_failure(self):
        # Arrange
        store_id = 1
        self.mock_store_repository.get_by_id.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.store_service.get_by_id(store_id)

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred where trying to get store by id")

    def test_create_success(self):
        # Arrange
        new_store_data = Store(name="New Store")
        expected_store = Store(id=1, name="New Store")
        self.mock_store_repository.create.return_value = expected_store

        # Act
        response = self.store_service.create(new_store_data)

        # Assert
        self.assertEqual(response['status'], 201)
        self.assertEqual(response['data']['id'], 1)
        self.assertEqual(response['data']['name'], "New Store")

    def test_create_failure(self):
        # Arrange
        new_store_data = Store(name="New Store")
        self.mock_store_repository.create.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.store_service.create(new_store_data)

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred where trying to add a new store")

    def test_update_success(self):
        # Arrange
        store_id = 1
        updated_store_data = StoreUpdate(name="Updated Store", opened=True)
        existing_store = Store(id=store_id, name="Old Store", opened=False)
        expected_updated_store = Store(id=store_id, name="Updated Store", opened=True)
        self.mock_store_repository.get_by_id.return_value = existing_store
        self.mock_store_repository.update.return_value = expected_updated_store

        # Act
        response = self.store_service.update(store_id, updated_store_data)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data']['id'], store_id)
        self.assertEqual(response['data']['name'], "Updated Store")
        self.assertEqual(response['data']['opened'], True)

    def test_update_not_found(self):
        # Arrange
        store_id = 999  # Assuming this ID doesn't exist
        updated_store_data = StoreUpdate(name="Updated Store", opened=True)
        self.mock_store_repository.get_by_id.return_value = None

        # Act
        response = self.store_service.update(store_id, updated_store_data)

        # Assert
        self.assertEqual(response['status'], 404)
        self.assertEqual(response['message'], "Store not has been searched")

    def test_update_failure(self):
        # Arrange
        store_id = 1
        updated_store_data = StoreUpdate(name="Updated Store", opened=True)
        self.mock_store_repository.get_by_id.return_value = Store(id=store_id, name="Old Store", opened=False)
        self.mock_store_repository.update.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.store_service.update(store_id, updated_store_data)

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred")

    def test_remove_success(self):
        # Arrange
        store_id = 1
        existing_store = Store(id=store_id, name="Store1", opened=True)
        self.mock_store_repository.get_by_id.return_value = existing_store

        # Act
        response = self.store_service.remove(store_id)

        # Assert
        self.assertEqual(response['status'], 200)

    def test_remove_not_found(self):
        # Arrange
        store_id = 999  # Assuming this ID doesn't exist
        self.mock_store_repository.get_by_id.return_value = None

        # Act
        response = self.store_service.remove(store_id)

        # Assert
        self.assertEqual(response['status'], 404)
        self.assertEqual(response['message'], "Store not has been searched")

    def test_remove_failure(self):
        # Arrange
        store_id = 1
        existing_store = Store(id=store_id, name="Store1", opened=True)
        self.mock_store_repository.get_by_id.return_value = existing_store
        self.mock_store_repository.remove.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.store_service.remove(store_id)

        # Assert
        self.assertEqual(response['status'], 500)
        self.assertEqual(response['message'], "A error occurred where trying delete a existing store")


if __name__ == '__main__':
    unittest.main()
