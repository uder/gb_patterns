import abc
import sqlite3
from windy.db.errors import DbRecordNotFoundException,DbCommitException,DbUpdateException,DbDeleteException
from windy.models.catalogue import Category,Course
from windy.include_patterns.singleton import Singleton
from windy.include_patterns.identity_map import IdentityMap

from pprint import pprint

class Mapper(metaclass=Singleton):
    load_from_db_priority = 100
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
    load_from_db_priority = 5

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
        self._get_childs_from_db()
        return result

    def _get_childs_from_db(self):
        for catid in self.identitymap.get_all_ids(Category):

            sql_query=f"SELECT catid,child_id FROM {self.children_table} WHERE catid={catid};"
            self.cursor.execute(sql_query)
            for row in self.cursor.fetchall():
                catid=row['catid']
                child_id=row['child_id']

                category=self.identitymap.get(Category,catid)
                child=self.identitymap.get(Category,child_id)
                if not child:
                    child = self.identitymap.get(Course, child_id)

                print(f"{catid} child: {child_id}")
                print(f"{category} child: {child}")
                print(f"{category.name} child: {child.name}")
                category.append(child,load_from_db=True)

    def get_by_id(self,catid):
        sql_query=f"SELECT * FROM {self.table} WHERE catid={catid};"
        result=self.identitymap.get(Category,catid)
        if not result:
            self.cursor.execute(sql_query)
            row=self.cursor.fetchone()
            if row:
                result=Category(row['name'],row['desc'],catid=catid)
                # result.set_catid(catid)
                # self.identitymap.set(catid, result)
            else:
                raise DbRecordNotFoundException(f'table={self.table}; catid={catid}')

        return result

    def insert(self,category):
        tups=category.get_tuples()
        sql_query=f"INSERT INTO {self.table} {tups[0]} VALUES {tups[1]};"
        self.cursor.execute(sql_query)
        for child in category.list_children():
            sql_query=f"INSERT INTO {self.children_table} (catid,child_id) VALUES ({category.catid},{child.catid});"
            self.cursor.execute(sql_query)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)

    def _get_diff_child_sets(self,category):
        catalogue_links_db=set()
        select_sql=f"SELECT catid, child_id FROM {self.children_table} WHERE catid={category.catid};"
        self.cursor.execute(select_sql)
        for row in self.cursor.fetchall():
            catalogue_links_db.add((row['catid'],row['child_id']))

        catalogue_links_obj=set()
        for obj in category.list_children():
            catalogue_links_obj.add((category.catid,obj.catid))

        links_to_insert=catalogue_links_obj-catalogue_links_db
        links_to_delete=catalogue_links_db-catalogue_links_obj

        # print(links_to_insert)
        # print(links_to_delete)
        return links_to_insert,links_to_delete

    def _child_links_insert(self,links_to_insert):
        for tup in links_to_insert:
            catid=tup[0]
            child_id=tup[1]
            sql_query= f"INSERT INTO {self.children_table} (catid, child_id) VALUES ({catid},{child_id});"
            self.cursor.execute(sql_query)

    def _child_links_delete(self,links_to_delete):
        for tup in links_to_delete:
            catid=tup[0]
            child_id=tup[1]
            sql_query=f"DELETE FROM {self.children_table} WHERE catid={catid} AND child_id={child_id}"
            self.cursor.execute(sql_query)

    def update(self,category):
        category_dict=category.get_dict()
        for key,value in category_dict.items():
            sql_query=f"UPDATE {self.table} SET {key} = '{value}' WHERE catid={category.catid}"
            # print (sql_query)
            self.cursor.execute(sql_query)
        link_to_insert,links_to_delete=self._get_diff_child_sets(category)
        self._child_links_insert(link_to_insert)
        self._child_links_delete(links_to_delete)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def delete(self,category):
        sql_query=f"DELETE FROM {self.table} WHERE catid={category.catid}"
        self.cursor.execute(sql_query)

        sql_query=f"SELECT * FROM {self.children_table} WHERE catid={category.catid}"
        links_to_delete=self.cursor.execute(sql_query)
        self._child_links_delete(links_to_delete)

        try:
            self.connection.commit()
        except Exception as err:
            raise DbDeleteException(err.args)

    def _check_orphan(self):
        pass

class CourseMapper(Mapper):
    load_from_db_priority = 1

    def __init__(self, connection):
        super().__init__(connection)
        self.table = 'course'

    @classmethod
    def mappers_key(cls):
        return Course

    def load_from_db(self):
        sql_query=f"SELECT * FROM {self.table};"
        self.cursor.execute(sql_query)
        result=[]
        for row in self.cursor.fetchall():
            catid=row['catid']
            name=row['name']
            duration=row['duration']

            course=self.identitymap.get(Course,catid)
            if not course:
                course=Course(name,duration,catid=catid)
            result.append(course)
        # self._get_childs_from_db(catid)
        return result

    def get_by_id(self,catid):
        sql_query=f"SELECT * FROM {self.table} WHERE catid={catid};"
        result=self.identitymap.get(Course,catid)
        if not result:
            self.cursor.execute(sql_query)
            row=self.cursor.fetchone()
            if row:
                result=Course(row['name'],row['duration'],catid=catid)
                # result.set_catid(catid)
                # self.identitymap.set(catid, result)
            else:
                raise DbRecordNotFoundException(f'table={self.table}; catid={catid}')

        return result

    def insert(self,course):
        tups=course.get_tuples()
        sql_query=f"INSERT INTO {self.table} {tups[0]} VALUES {tups[1]};"
        self.cursor.execute(sql_query)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)

    def update(self,course):
        course_dict=course.get_dict()
        for key,value in course_dict.items():
            sql_query=f"UPDATE {self.table} SET {key} = '{value}' WHERE catid={course.catid}"
            # print (sql_query)
            self.cursor.execute(sql_query)
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def delete(self,course):
        sql_query=f"DELETE FROM {self.table} WHERE catid={course.catid}"
        self.cursor.execute(sql_query)

        try:
            self.connection.commit()
        except Exception as err:
            raise DbDeleteException(err.args)

    def _check_orphan(self):
        pass