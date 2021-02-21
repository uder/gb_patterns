import abc

class User():
    users={}

    @classmethod
    def create(cls,name,role):
        # if cls.users.get(name,None):
        #     return None
        roles=cls._get_roles()
        user=roles[role](name)
        cls.users.update({name:user})
        return user

    @classmethod
    def _get_roles(cls):
        roles={
            'student': Student,
            'teacher': Teacher
        }
        return roles

    @classmethod
    def users_list(cls):
        keys=cls.users.keys()
        if keys:
            return keys
        else:
            return []

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return f'User(Name: {self.name} Role: {self.__class__.__name__} Courses: {str(self.get_courses_list())})'

    @abc.abstractmethod
    def sign(self,course):
        pass

    @abc.abstractmethod
    def unsign(self,course):
        pass

    @abc.abstractmethod
    def get_courses_list(self):
        pass

class Student(User):
    def __init__(self,name):
        super().__init__(name)
        self._student_courses=set()

    def sign(self,course):
        self._student_courses.add(course)

    def unsign(self,course):
        self._student_courses.discard(course)

    def get_courses_list(self):
        return self._student_courses

    def say(self):
        print (f'Im Student, my name is {self.name}')

class Teacher(User):
    def say(self):
        print (f'Im Teacher, my name is {self.name}')

    def sign(self,course):
        pass

    def unsign(self,course):
        pass

    def get_courses_list(self):
        pass
