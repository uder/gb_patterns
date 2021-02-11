
class User():
    @classmethod
    def create(cls,name,role):
        if __class__.__name__!='User':
            print (f'ERROR: invoke from {__class__.__name__}')
            return None
        roles=cls._get_roles()
        return  roles[role](name)

    @classmethod
    def _get_roles(cls):
        roles={
            'student': Student,
            'teacher': Teacher
        }
        return roles

    def __init__(self,name):
        self.name=name


class Student(User):
    def say(self):
        print (f'Im Student, my name is {self.name}')

class Teacher(User):
    def say(self):
        print (f'Im Teacher, my name is {self.name}')