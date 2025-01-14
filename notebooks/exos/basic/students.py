class Student:
    """
    a class to demonstrate how to define
    a custom class that can be used in a set or a dict
    (and that can be sorted too, btw)

    try and run it without the last 3 dunder methods to see what happens
    """

    def __init__(self, first_name, last_name, grade=None):
        self.first_name = first_name
        self.last_name = last_name
        self.grade = grade

    # pretty print
    def __repr__(self):
        return f"<{self.first_name} {self.last_name} ({self.grade})>"

    # hash on first and last name
    def __hash__(self):
        return hash( (self.first_name, self.last_name) )

    # the protocol for hashable objets require this to be defined too
    def __eq__(self, other):
        return self.first_name == other.first_name and self.last_name == other.last_name

    # sort on grades
    def __lt__(self, other):
        return self.grade < other.grade

#### usage


print(10*'=', 'a set containing students')

s1 = Student('John', 'Doe', 12)
s2 = Student('Jane', 'Doe', 15)
s3 = Student('Jean', 'Dupont', 11)
s4 = Student('Marie', 'Martin', 14)

# can use a set to store students
students = {s1, s2, s3}

print(f"{s1 in students=}")
print(f"{s4 in students=}")

s1.grade = 13
print(f"after grade change {s1 in students=}")



print(10*'=', 'dict works too')

grades_by_students = {s: s.grade for s in students}
print(f"{grades_by_students[s2]=}")

# this one would not work if we had not defined __hash__ and __eq__
s1bis = Student('John', 'Doe')
print(f"{s1bis in students=} and {grades_by_students[s1bis]=}")


print(10*'=', 'sorting')

students = {s1, s2, s3, s4}
print(f"{sorted(students)=}")
