class VacancyMixin:

    def __init__(self):
        print(repr(self))

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.id}, {self.name}, {self.area}, {self.area}, {self.salary}, "
                f"{self.description}, {self.snippet})")
