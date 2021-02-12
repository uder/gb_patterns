from windy.include_patterns.prototype import PrototypeMixin

class Course(PrototypeMixin):
    courses={}

    @classmethod
    def get_course_by_name(self,name):
        course=self.courses.get(name,None)
        return course

    def __init__(self,name,duration):
        self.name=name
        self.duration=duration

        self.courses.update({self.name: self})

    def __repr__(self):
        return f"Course(Name: {self.name}, Duration: {self.duration})"

    def set_name(self, name):
        if not self.courses.get(name, None):
            self.name=name
            result=True
        else:
            result=False

        return result

    def student_count(self):
        pass