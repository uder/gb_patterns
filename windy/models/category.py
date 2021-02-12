class Category():
    def __init__(self,name,desc):
        self.name=name
        self.desc=desc

    def __repr__(self):
        return f"Category(Name: {self.name}, Description: {self.desc})"

    def course_count(self):
        pass