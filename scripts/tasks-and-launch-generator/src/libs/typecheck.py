from .validatable import Validatable

class TypeCheck(Validatable):
    def __init__(self, value_type):
        # type: (type) -> TypeCheck
        self.value_type = value_type

    def validate(self, value):
        # print(value, self.value_type.__name__)
        if (isinstance(value, self.value_type)):
            return
        else:
            return TypeError("The " + str(value) + " is not " + self.value_type.__name__ + ".")
