import unittest
from modules.clients.client_model import ClientCreate, ClientUpdate


class TestClientModel(unittest.TestCase):

    def test_client_create(self):
        data = {
            "name": "John Doe",
            "money": 1000.0
        }
        client_create = ClientCreate(**data)
        self.assertEqual(client_create.name, "John Doe")
        self.assertEqual(client_create.money, 1000.0)

    def test_client_update(self):
        data = {
            "name": "Jane Doe",
            "money": 1500.0
        }
        client_update = ClientUpdate(**data)
        self.assertEqual(client_update.name, "Jane Doe")
        self.assertEqual(client_update.money, 1500.0)


if __name__ == '__main__':
    unittest.main()
