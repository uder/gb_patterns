import abc
import windy.include_patterns.mark_mixin
from windy.include_patterns.prototype import PrototypeMixin


class Catalogue(windy.include_patterns.mark_mixin.MarkMixin, metaclass=abc.ABCMeta):
    def __init__(self,name):
        from windy.include_patterns.identity_map import IdentityMap
        self.name=name
        self.identitymap=IdentityMap()

    @abc.abstractmethod
    def list_children(self):
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
                raise f"Error catalogue object with {catid} already exists"

        self.desc=desc
        self._children=[]
        self.identitymap.set(self.catid,self)

    def get_last_catid(self):
        ids=self.identitymap.get_all_ids(self.__class__)
        if ids:
            last_catid=max(ids)
        else:
            last_catid=0

        return last_catid

    def auto_set_catid(self):
        catid=self.get_last_catid()+1
        return catid

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

    def append(self,object):
        if isinstance(object,Catalogue):
            self._children.append(object)

    def remove(self,object):
        index=self._children.index(object)
        if index:
            self._children.remove(index)

    def __repr__(self):
        return f"Category(CatID: {self.catid} Name: {self.name}, Description: {self.desc})"

    def course_count(self):
        pass


class Course(Catalogue,PrototypeMixin):
    courses={}

    @classmethod
    def get_course_by_name(self,name):
        course=self.courses.get(name,None)
        return course

    @classmethod
    def get_courses_list(self):
        keys=self.courses.keys()
        if keys:
            return keys
        else:
            return []

    @classmethod
    def get_courses(cls):
        return cls.courses

    def __init__(self,name,duration):
        super().__init__(name)
        self.duration=duration
        self.courses.update({self.name: self})

    def list_children(self):
        return []

    def __repr__(self):
        return f"Course(Name: {self.name}, Duration: {self.duration})"

    def set_name(self, name):
        if not self.courses.get(name, None):
            self.name=name
            self.courses.update({self.name:self})
            result=True
        else:
            result=False

        return result

    def set_duration(self,duration):
        self.duration=duration

    def student_count(self):
        pass