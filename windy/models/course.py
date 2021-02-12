class Course():
    def __init__(self,name,duration):
        self.name=name
        self.duration=duration

    def __repr__(self):
        return f"Course(Name: {self.name}, Duration: {self.duration})"

    def student_count(self):
        pass