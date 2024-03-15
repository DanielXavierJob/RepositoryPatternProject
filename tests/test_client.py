import unittest
from modules.clients.client import Client


class TestClient(unittest.TestCase):

    def test_client_attributes(self):
        client = Client(name='John Doe', money=100.0)
        self.assertEqual(client.name, 'John Doe')
        self.assertEqual(client.money, 100.0)

    def test_to_dict(self):
        client = Client(name='John Doe', money=100.0)
        client_dict = client.to_dict()
        self.assertEqual(client_dict['name'], 'John Doe')
        self.assertEqual(client_dict['money'], 100.0)

        # Check for the presence of other attributes
        self.assertIn('id', client_dict)
        self.assertIn('created_at', client_dict)
        self.assertIn('updated_at', client_dict)
        self.assertIn('deleted_at', client_dict)


if __name__ == '__main__':
    unittest.main()
