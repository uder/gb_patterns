import abc
import sqlite3
# from windy.models.category import Category
from .category_mapper import Category,CategoryMapper


class Mapper(metaclass=abc.ABCMeta):
    mappers={
        Category: CategoryMapper
    }

    @classmethod
    def get_mapper(cls,obj):
        mapper=cls.mappers.get(obj.__class__,None)
        return mapper

    def __init__(self,connection):
        self.connection = connection
        self.connection.row_factory=sqlite3.Row
        self.cursor = connection.cursor()

    @abc.abstractmethod
    def load_from_db(self):
        pass

    @abc.abstractmethod
    def get_by_id(self,id):
        pass

    @abc.abstractmethod
    def insert(self,object):
        pass

    @abc.abstractmethod
    def update(self,object):
        pass

    @abc.abstractmethod
    def delete(self,object):
        pass