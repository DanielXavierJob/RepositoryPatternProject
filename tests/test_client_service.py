import unittest
from unittest.mock import MagicMock

from sqlalchemy.exc import IntegrityError

from modules.clients.client_model import ClientUpdate
from modules.clients.client_service import ClientService
from modules.clients.client import Client


class TestClientService(unittest.TestCase):

    def setUp(self):
        self.client_service = ClientService()
        self.mock_repository = MagicMock()
        self.client_service.client_repository = self.mock_repository

    def test_get_all_success(self):
        # Arrange
        expected_clients = [Client(id=1, name="Client1", money=100), Client(id=2, name="Client2", money=200)]
        self.mock_repository.get_all.return_value = expected_clients

        # Act
        response = self.client_service.get_all()

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(len(response['data']), 2)

    def test_get_all_failure(self):
        # Arrange
        self.mock_repository.get_all.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.client_service.get_all()
        # Assert
        self.assertEqual(response['status'], 500)

    def test_get_by_id_success(self):
        # Arrange
        client_id = 1
        expected_client = Client(id=client_id, name="John Doe", money=100)
        self.mock_repository.get_by_id.return_value = expected_client

        # Act
        response = self.client_service.get_by_id(client_id)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data']['id'], client_id)

    def test_get_by_id_not_found(self):
        # Arrange
        client_id = 999  # Assuming this ID doesn't exist
        self.mock_repository.get_by_id.return_value = None

        # Act
        response = self.client_service.get_by_id(client_id)

        # Assert
        self.assertEqual(response['status'], 404)

    def test_get_by_id_failure(self):
        # Arrange
        client_id = 1
        self.mock_repository.get_by_id.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.client_service.get_by_id(client_id)

        # Assert
        self.assertEqual(response['status'], 500)

    def test_create_success(self):
        # Arrange
        new_client_data = Client(name="John Doe", money=100)
        expected_client = Client(id=1, name="John Doe", money=100)
        self.mock_repository.create.return_value = expected_client

        # Act
        response = self.client_service.create(new_client_data)

        # Assert
        self.assertEqual(response['status'], 201)
        self.assertEqual(response['data']['id'], 1)
        self.assertEqual(response['data']['name'], "John Doe")
        self.assertEqual(response['data']['money'], 100)

    def test_create_failure(self):
        # Arrange
        new_client_data = Client(name="John Doe", money=100)
        self.mock_repository.create.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.client_service.create(new_client_data)

        # Assert
        self.assertEqual(response['status'], 500)
    def test_update_success(self):
        # Arrange
        client_id = 1
        updated_client_data = ClientUpdate(name="John Doe", money=200)
        existing_client = Client(id=client_id, name="Old Name", money=100)
        expected_updated_client = Client(id=client_id, name="John Doe", money=200)
        self.mock_repository.update.return_value = expected_updated_client
        self.mock_repository.get_by_id.return_value = existing_client

        # Act
        response = self.client_service.update(client_id, updated_client_data)

        # Assert
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data']['id'], client_id)
        self.assertEqual(response['data']['name'], "John Doe")
        self.assertEqual(response['data']['money'], 200)

    def test_update_not_found(self):
        # Arrange
        client_id = 999  # Assuming this ID doesn't exist
        updated_client_data = ClientUpdate(name="John Doe", money=200)
        self.mock_repository.get_by_id.return_value = None

        # Act
        response = self.client_service.update(client_id, updated_client_data)

        # Assert
        self.assertEqual(response['status'], 404)

    def test_update_failure(self):
        # Arrange
        client_id = 1
        updated_client_data = ClientUpdate(name="John Doe", money=200)
        self.mock_repository.get_by_id.return_value = Client(id=client_id, name="Old Name", money=100)
        self.mock_repository.update.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.client_service.update(client_id, updated_client_data)

        # Assert
        self.assertEqual(response['status'], 500)

    def test_remove_success(self):
        # Arrange
        client_id = 1
        existing_client = Client(id=client_id, name="John Doe", money=100)
        self.mock_repository.get_by_id.return_value = existing_client

        # Act
        response = self.client_service.remove(client_id)

        # Assert
        self.assertEqual(response['status'], 200)

    def test_remove_not_found(self):
        # Arrange
        client_id = 999  # Assuming this ID doesn't exist
        self.mock_repository.get_by_id.return_value = None

        # Act
        response = self.client_service.remove(client_id)

        # Assert
        self.assertEqual(response['status'], 404)

    def test_remove_failure(self):
        # Arrange
        client_id = 1
        existing_client = Client(id=client_id, name="John Doe", money=100)
        self.mock_repository.get_by_id.return_value = existing_client
        self.mock_repository.remove.side_effect = IntegrityError('None', 'None', 'unit-test')

        # Act
        response = self.client_service.remove(client_id)

        # Assert
        self.assertEqual(response['status'], 500)

if __name__ == '__main__':
    unittest.main()
