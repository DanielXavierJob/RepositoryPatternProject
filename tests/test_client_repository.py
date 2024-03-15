import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import scoped_session, sessionmaker
from database.db import db_connection
from modules.clients.client_repository import ClientRepository
from modules.clients.client import Client


class TestClientRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = scoped_session(sessionmaker())
        db_connection.session = cls.session

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def setUp(self):
        self.repository = ClientRepository()

    @patch('modules.clients.client_repository.db_connection.session')
    def test_get_all(self, mock_session):
        mock_session.query().filter().all.return_value = [
            Client(id=1, name='Client 1'),
            Client(id=2, name='Client 2')
        ]
        clients = self.repository.get_all()
        self.assertEqual(len(clients), 2)

    @patch('modules.clients.client_repository.db_connection.session')
    def test_get_by_id(self, mock_session):
        mock_session.query().filter().first.return_value = Client(id=1, name='Client 1')
        client = self.repository.get_by_id(id=1)
        self.assertIsNotNone(client)
        self.assertEqual(client.id, 1)
        self.assertEqual(client.name, 'Client 1')

    @patch('modules.clients.client_repository.db_connection.session')
    def test_create(self, mock_session):
        new_client = Client(id=3, name='New Client')
        self.repository.create(new_client)
        mock_session.add.assert_called_once_with(new_client)
        mock_session.commit.assert_called_once()

    @patch('modules.clients.client_repository.db_connection.session')
    def test_update(self, mock_session):
        updated_client = Client(id=1, name='Updated Client')
        mock_session.query().get.return_value = updated_client
        self.repository.update(updated_client)
        mock_session.commit.assert_called_once()

    @patch('modules.clients.client_repository.db_connection.session')
    def test_remove(self, mock_session):
        # Mocking a client object
        client_to_delete = MagicMock()

        # Patching the session to return our mock session
        with patch('modules.clients.client_repository.db_connection.session', mock_session):
            # Creating an instance of ClientRepository
            client_repository = ClientRepository()

            # Calling the remove method
            client_repository.remove(client_to_delete)

        # Asserting that soft_delete was called once with client_to_delete
        client_to_delete.soft_delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()
