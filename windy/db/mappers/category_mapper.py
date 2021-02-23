import windy.db.mappers.mapper
import windy.models.category
from windy.db.errors import DbRecordNotFoundException,DbCommitException,DbUpdateException,DbDeleteException

class CategoryMapper(windy.db.mappers.mapper.Mapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.table = 'category'

    def load_from_db(self):
        sql_query=f"SELECT * FROM {self.table};"
        self.cursor.execute(sql_query)
        result=[]
        for row in self.cursor.fetchall():
            catid=row['catid']
            name=row['name']
            desc=row['desc']
            # id, catid, name, description = row
            category=windy.models.category.Category(name,desc)
            category.set_catid(catid)
            result.append(category)
        return result

    def get_by_id(self,catid):
        sql_query=f"SELECT * FROM {self.table} WHERE catid={catid};"
        self.cursor.execute(sql_query)
        row=self.cursor.fetchone()
        if row:
            result=windy.models.category.Category(row['name'],row['desc'])
            result.set_catid(catid)
            return result
        else:
            raise DbRecordNotFoundException(f'table={self.table}; catid={catid}')

    def insert(self,category):
        tups=category.get_tuples()
        sql_query=f"INSERT INTO {self.table} ({tups[0]}) VALUES ({tups[1]});"
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
