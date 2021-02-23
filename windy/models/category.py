from .catalogue import Catalogue

class Category(Catalogue):
    # auto_catid=0
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
        catid=self.catid
        self.catid+=1
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
        for k,v in self.get_dict():
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
        return f"Category(Name: {self.name}, Description: {self.desc})"

    def course_count(self):
        pass
