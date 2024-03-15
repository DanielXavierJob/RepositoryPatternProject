import unittest

from standard.repository import Repository

class ConcreteRepository(Repository):
    def get_all(self, **kwargs):
        """Implementation of the get_all method"""
        raise NotImplementedError

    def get_by_id(self, **kwargs):
        """Implementation of the get_by_id method"""
        raise NotImplementedError

    def create(self, **kwargs):
        """Implementation of the create method"""
        raise NotImplementedError

    def update(self, **kwargs):
        """Implementation of the update method"""
        raise NotImplementedError

    def remove(self, **kwargs):
        """Implementation of the remove method"""
        raise NotImplementedError


class TestRepository(unittest.TestCase):
    def setUp(self):
        # Create an instance of Repository to test
        self.repository = ConcreteRepository()

    def test_get_all(self):
        # Test the get_all method
        with self.assertRaises(NotImplementedError):
            self.repository.get_all()

    def test_get_by_id(self):
        # Test the get_by_id method
        with self.assertRaises(NotImplementedError):
            self.repository.get_by_id()

    def test_create(self):
        # Test the create method
        with self.assertRaises(NotImplementedError):
            self.repository.create()

    def test_update(self):
        # Test the update method
        with self.assertRaises(NotImplementedError):
            self.repository.update()

    def test_remove(self):
        # Test the remove method
        with self.assertRaises(NotImplementedError):
            self.repository.remove()
if __name__ == '__main__':
    unittest.main()