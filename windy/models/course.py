from windy.include_patterns.prototype import PrototypeMixin
from .catalogue import Catalogue

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