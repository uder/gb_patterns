import abc
import windy.include_patterns.mark_mixin
from windy.include_patterns.prototype import PrototypeMixin

class Catalogue(windy.include_patterns.mark_mixin.MarkMixin, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_children(self):
        pass

class Category(Catalogue):
    auto_catid=0
    categories={}
    root={}

    @classmethod
    def get_last_catid(cls):
        last_catid=0
        for category in cls.categories.values():
            if category.catid>last_catid:
                last_catid=category.catid+1

        return last_catid

    @classmethod
    def list_root(cls):
        keys=cls.root.keys()
        if keys:
            return keys
        else:
            return []

    @classmethod
    def get_category_by_name(cls,name):
        category=cls.categories.get(name,None)
        return category

    @classmethod
    def categories_list(cls):
        keys=cls.categories.keys()
        if keys:
            return keys
        else:
            return []

    @classmethod
    def get_categories(cls):
        return cls.categories

    def __init__(self,name,desc):
        self.catid=self.auto_catid()
        self.name=name
        self.desc=desc
        self._children=[]
        self.categories.update({self.name:self})

    def auto_catid(self):
        self.auto_catid=self.get_last_catid()
        catid=self.auto_catid
        self.auto_catid+=1
        return catid

    def set_catid(self,catid):
        self.catid=catid

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

    # def set_root(self):
    #     self.root.update({self.name,self})

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
        self.name=name
        self.duration=duration
        # self._category=None
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

    # def set_category(self,category):
    #     if isinstance(Catalogue,category):
    #         self._category=category
    #         return True
    #     else:
    #         return False

    def set_duration(self,duration):
        self.duration=duration

    def student_count(self):
        pass