# repository.py

from abc import abstractmethod
from abc import ABC


class Repository(ABC):
    @abstractmethod
    def get_all(self, **kwargs):
        """Get all items from repository"""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, **kwargs):
        """Get item by id from repository"""
        raise NotImplementedError

    @abstractmethod
    def create(self, **kwargs):
        """Add item in repository"""
        raise NotImplementedError

    @abstractmethod
    def update(self, **kwargs):
        """Returns all items in repository"""
        raise NotImplementedError

    @abstractmethod
    def remove(self, **kwargs):
        """Remove item by id from repository"""
        raise NotImplementedError

