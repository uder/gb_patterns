class Category():
    categories=[]
    categories=['fisrt','second']

    @classmethod
    def categories_list(self):
        return self.categories

    def __init__(self,name,desc):
        self.name=name
        self.desc=desc
        self.categories.append(name)

    def __repr__(self):
        return f"Category(Name: {self.name}, Description: {self.desc})"




    def course_count(self):
        pass