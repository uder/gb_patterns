from windy.include_patterns.singleton import Singleton
from windy.models.catalogue import Catalogue,Category,Course
from windy.models.user import User

# from pprint import pprint

class IdentityMap(metaclass=Singleton):
    identities = {
        Catalogue: dict(),
        Category: None,
        Course: None,
        User: dict()
    }

    def __init__(self):
        self.identities[Category]=self.identities[Catalogue]
        self.identities[Course]=self.identities[Course]

    def get(self,klass,id):
        # result=None
        try:
            result=self.identities.get(klass).get(id,None)
        except Exception as err:
            raise err

        return result

    def set(self,id,obj):
        self.identities.get(obj.__class__).update({id:obj})

    def get_all_ids(self,klass):
        return self.identities.get(klass).keys()

    def get_by_name(self,klass,name):
        result=None
        for obj in self.identities.get(klass).values():
            if obj.name==name and obj.__class__ is klass:
                result=obj
                break

        return result