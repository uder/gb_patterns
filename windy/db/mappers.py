import abc
import sqlite3
# import windy.models.catalogue
from windy.db.errors import DbRecordNotFoundException,DbCommitException,DbUpdateException,DbDeleteException
from windy.models.catalogue import Category,Catalogue
from windy.include_patterns.singleton import Singleton
from windy.include_patterns.identity_map import IdentityMap

class Mapper(metaclass=Singleton):
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
        self.identitymap=IdentityMap()

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
        self.children_table='catalogue_children'

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



            category=self.identitymap.get(Category,catid)
            if not category:
                category=Category(name,desc,catid=catid)
            result.append(category)
        return result

    def _get_childs_from_db(self,catid):
        sql_query=f"SELECT catid,child_id FROM {self.children_table};"
        self.cursor.execute(sql_query)
        for row in self.cursor.fetchall():
            catid=row['catid']
            child_id=row['child_id']



    def get_by_id(self,catid):
        sql_query=f"SELECT * FROM {self.table} WHERE catid={catid};"
        result=self.identitymap.get(Category,catid)
        if not result:
            self.cursor.execute(sql_query)
            row=self.cursor.fetchone()
            if row:
                result=Category(row['name'],row['desc'])
                result.set_catid(catid)
                self.identitymap.set(catid, result)
            else:
                raise DbRecordNotFoundException(f'table={self.table}; catid={catid}')

        return result

    def insert(self,category):
    # def insert(self):
        tups=category.get_tuples()
        sql_query=f"INSERT INTO {self.table} {tups[0]} VALUES {tups[1]};"
        self.cursor.execute(sql_query)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)

    def _insert_children(self,category):
        for child in category.list_children():
            sql_query= f"INSERT INTO {self.children_table} (catid, child_id) VALUES ({category.catid},{child.catid});"
            print(sql_query)
            self.cursor.execute(sql_query)
            # print("Ok child rquest")
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)


    def update(self,category):
        category_dict=category.get_dict()
        for key,value in category_dict.items():
            sql_query=f"UPDATE {self.table} SET {key} = '{value}' WHERE catid={category.catid}"
            # print (sql_query)
            self.cursor.execute(sql_query)
        self._insert_children(category)
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
