import abc
import sqlite3
# import windy.models.catalogue
from windy.db.errors import DbRecordNotFoundException,DbCommitException,DbUpdateException,DbDeleteException
from windy.models.catalogue import Category

class Mapper(metaclass=abc.ABCMeta):
    # mappers={
    #     Category: CategoryMapper
    # }
    mappers={}
    @classmethod
    def register_mappers(cls):
        for subc in cls.__subclasses__():
            cls.mappers.update({subc.mappers_key():subc})

    @classmethod
    def get_mapper(cls,obj):
        mapper=cls.mappers.get(obj.__class__,None)
        return mapper

    def __init__(self,connection):
        self.register_mappers()
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

    @property
    def mappers_key(self):
        return None

class CategoryMapper(Mapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.table = 'category'

    @classmethod
    def mappers_key(cls):
        return Category

    def load_from_db(self):
        sql_query=f"SELECT * FROM {self.table};"
        self.cursor.execute(sql_query)
        result=[]
        for row in self.cursor.fetchall():
            catid=row['catid']
            name=row['name']
            desc=row['desc']
            # id, catid, name, description = row
            category=Category(name,desc)
            category.set_catid(catid)
            result.append(category)
        return result

    def get_by_id(self,catid):
        sql_query=f"SELECT * FROM {self.table} WHERE catid={catid};"
        self.cursor.execute(sql_query)
        row=self.cursor.fetchone()
        if row:
            result=Category(row['name'],row['desc'])
            result.set_catid(catid)
            return result
        else:
            raise DbRecordNotFoundException(f'table={self.table}; catid={catid}')

    def insert(self,category):
    # def insert(self):
        tups=category.get_tuples()
        sql_query=f"INSERT INTO {self.table} {tups[0]} VALUES {tups[1]};"
        self.cursor.execute(sql_query)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)

    def update(self,category):
        category_dict=category.get_dict()
        for key,value in category_dict.item():
            sql_query=f"UPDATE {self.table} SET {key} = {value}"
            self.cursor.execute(sql_query)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def delete(self,category):
        sql_query=f"DELETE FROM {self.table} WHERE catid={category.catid}"
        self.cursor.execute(sql_query)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbDeleteException(err.args)
