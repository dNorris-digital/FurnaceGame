
class Person():
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.characteristics = []
        self.mother = ""
        self.father = ""
        self.gender = gender

    def SetFeatures(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def Birthday(self):
        self.age+=1

family = []
family.append(Person("jane", 34, "F"))
family.append(Person("Vivian", 7, "F"))
family.append(Person("ariana",12 , "F"))
family.append(Person("jared", 33, "M"))
family.append(Person("gavin", 10, "M"))

print(family)