import abc
import windy.include_patterns.mark_mixin
from windy.include_patterns.prototype import PrototypeMixin

class CatalogueException(Exception):
    def __init__(self, message):
        super().__init__(f'Catalogue object error: {message}')

class Catalogue(windy.include_patterns.mark_mixin.MarkMixin, metaclass=abc.ABCMeta):
    def __init__(self,name):
        from windy.include_patterns.identity_map import IdentityMap
        self.name=name
        self.identitymap=IdentityMap()

    def auto_set_catid(self):
        ids=self.identitymap.get_all_ids(self.__class__)
        if ids:
            last_catid=max(ids)+1
        else:
            last_catid=0
        # catid=self.get_last_catid()+1
        return last_catid

    @abc.abstractmethod
    def list_children(self):
        pass

    @abc.abstractmethod
    def get_dict(self):
        pass

    @abc.abstractmethod
    def get_tuples(self):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass

class Category(Catalogue):
    def __init__(self,name,desc,catid=None):
        super().__init__(name)
        if catid is None:
            self.catid = self.auto_set_catid()
        else:
            if not self.identitymap.get(self.__class__,catid):
                self.catid=catid
            else:
                raise CatalogueException(f"Category with catid={catid} already exists")

        self.desc=desc
        self._children=[]
        self.identitymap.set(self.catid,self)

    def get_dict(self):
        result={}
        result.update({'catid':self.catid})
        result.update({'name':self.name})
        result.update({'desc':self.desc})
        return result

    def get_tuples(self):
        keys_list=[]
        values_list=[]
        for k,v in self.get_dict().items():
            keys_list.append(k)
            values_list.append(v)
        result=[]
        result.append(tuple(keys_list))
        result.append(tuple(values_list))
        # result.append(('catid','name','description'))
        # result.append((self.catid,self.name,self.desc))
        return result

    def list_children(self):
        return self._children

    def append(self,object,load_from_db=False):
        if isinstance(object,Catalogue):
            self._children.append(object)
            if not load_from_db:
                self.mark_dirty()


    def remove(self,object):
        try:
            self._children.remove(object)
            self.mark_dirty()
        except:
            raise CatalogueException(f"Cant remove {object}")

    def __repr__(self):
        return f"Category(CatID: {self.catid} Name: {self.name}, Description: {self.desc} Children: {self._children})"

    def course_count(self):
        pass


class Course(Catalogue,PrototypeMixin):
    def __init__(self,name,duration,catid=None):
        super().__init__(name)
        if catid is None:
            self.catid = self.auto_set_catid()
        else:
            if not self.identitymap.get(self.__class__,catid):
                self.catid=catid
            else:
                raise CatalogueException(f"Course with catid={catid} already exists")
        self.duration=duration
        self.identitymap.set(self.catid,self)

    def list_children(self):
        return []

    def __repr__(self):
        return f"Course(Name: {self.name}, Duration: {self.duration})"

    def get_dict(self):
        result={}
        result.update({'catid':self.catid})
        result.update({'name':self.name})
        result.update({'duration':self.duration})
        return result

    def get_tuples(self):
        keys_list=[]
        values_list=[]
        for k,v in self.get_dict().items():
            keys_list.append(k)
            values_list.append(v)
        result=[]
        result.append(tuple(keys_list))
        result.append(tuple(values_list))
        # result.append(('catid','name','description'))
        # result.append((self.catid,self.name,self.desc))
        return result

    def set_name(self, name):
        if not self.identitymap.get_by_name(Course,name):
            self.name=name
            self.identitymap.set(self.catid,self)
            self.mark_dirty()
            result=True
        else:
            result=False

        return result

    def set_duration(self,duration):
        self.duration=duration
        self.mark_dirty()

    def student_count(self):
        pass
