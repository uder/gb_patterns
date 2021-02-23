import windy.db.mappers.mapper

class UnitOfWork():
    _current=None

    @classmethod
    def set_current(cls):
        cls._current=cls()

    @classmethod
    def get_current(cls):
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
        Mapper=windy.db.mappers.mapper.Mapper
        for obj in self.new_objects:
            mapper=Mapper.mappers.get(obj.__class__,None)
            if mapper:
                mapper.insert(obj)

    def update_dirty(self):
        Mapper=windy.db.mappers.mapper.Mapper
        for obj in self.dirty_objects:
            mapper=Mapper.mappers.get(obj.__class__,None)
            if mapper:
                mapper.update(obj)

    def delete_remove(self):
        Mapper=windy.db.mappers.mapper.Mapper
        for obj in self.remove_objects:
            mapper=Mapper.mappers.get(obj.__class__,None)
            if mapper:
                mapper.delete(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_remove()
