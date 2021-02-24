# import windy.db.mappers

class UnitOfWork():
    _current=None
    _mapper=None
    _connection=None

    @classmethod
    def set_current(cls):
        cls._current=cls()

    @classmethod
    def get_current(cls):
        from windy.db.mappers import Mapper
        from windy.db.connection import create_connection
        cls._mapper=Mapper
        cls._mapper.register_mappers()
        cls._connection=create_connection()
        return cls._current

    def __init__(self):
        self.new_objects=[]
        self.dirty_objects=[]
        self.remove_objects=[]

    def add_new(self,obj):
        self.new_objects.append(obj)

    def add_dirty(self,obj):
        self.dirty_objects.append(obj)

    def add_remove(self,obj):
        self.remove_objects.append(obj)

    def insert_new(self):
        for obj in self.new_objects:
            mapper=self._mapper.mappers.get(obj.__class__,None)(self._connection)
            if mapper:
                mapper.insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            mapper=self._mapper.mappers.get(obj.__class__,None)(self._connection)
            if mapper:
                mapper.update(obj)

    def delete_remove(self):
        for obj in self.remove_objects:
            mapper=self._mapper.mappers.get(obj.__class__,None)(self._connection)
            if mapper:
                mapper.delete(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_remove()
