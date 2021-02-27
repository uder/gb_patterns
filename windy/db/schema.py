import abc
# from windy.db.errors import DbCreateTableException


class Table(metaclass=abc.ABCMeta):
    @classmethod
    def tables_list(cls):
        t_list=cls.__subclasses__()
        return t_list

    def __init__(self,connection):
        self.connection=connection
        self.cursor=connection.cursor()

    @abc.abstractmethod
    def create(self,drop_if_exists=False):
        pass

    # @abc.abstractmethod
    # def drop(self):
    #     pass
    def drop(self):
        sql_query=f"""DROP TABLE IF EXISTS {self.table}"""
        self.cursor.execute(sql_query)
        self.connection.commit()

class CategoryTable(Table):
    def __init__(self,connection):
        super().__init__(connection)
        self.table='category'

    def create(self, drop_if_exists=False):
        if drop_if_exists:
            self.drop()
        # else:
        #     raise DbCreateTableException(self.table)
        sql_query=f"""CREATE TABLE IF NOT EXISTS {self.table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        catid INTEGER NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        desc TEXT
                    )"""
        self.cursor.execute(sql_query)
        self.connection.commit()

    # def drop(self):
    #     sql_query=f"""DROP TABLE IF EXISTS {self.table}"""
    #     self.cursor.execute(sql_query)
    #     self.connection.commit()


class CatalogueChildren(Table):
    def __init__(self,connection):
        super().__init__(connection)
        self.table='catalogue_children'

    def create(self, drop_if_exists=False):
        if drop_if_exists:
            self.drop()
        sql_query=f"""CREATE TABLE IF NOT EXISTS {self.table} (
                        catid INTEGER NOT NULL,
                        child_id INTEGER NOT NULL,
                        UNIQUE(catid,child_id)
                    )"""
        self.cursor.execute(sql_query)
        self.connection.commit()

    # def drop(self):
    #     sql_query=f"""DROP TABLE IF EXISTS {self.table}"""
    #     self.cursor.execute(sql_query)
    #     self.connection.commit()


class DbInit():
    def __init__(self, connection, drop_if_exsists = False):
        self.connection=connection
        self.drop_if_exsists = drop_if_exsists

    def create_tables(self):
        for table in Table.tables_list():
            table_object=table(self.connection)
            table_object.create(self.drop_if_exsists)

class CourseTable(Table):
    def __init__(self,connection):
        super().__init__(connection)
        self.table='course'

    def create(self, drop_if_exists=False):
        if drop_if_exists:
            self.drop()
        # else:
        #     raise DbCreateTableException(self.table)
        sql_query=f"""CREATE TABLE IF NOT EXISTS {self.table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        catid INTEGER NOT NULL UNIQUE,
                        name TEXT NOT NULL UNIQUE,
                        duration TEXT
                    )"""
        self.cursor.execute(sql_query)
        self.connection.commit()
