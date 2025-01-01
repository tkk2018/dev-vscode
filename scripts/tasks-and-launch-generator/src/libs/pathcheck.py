import os
from .typecheck import TypeCheck

class PathCheck(TypeCheck):
    def __init__(self, isDiretory):
        super(PathCheck, self).__init__(str)
        self.isDirectory = isDiretory

    def validate(self, value):
        error = super(PathCheck, self).validate(value)
        if error is not None:
            return error

        if (self.isDirectory):
            if (not os.path.isdir(value)):
                error = IOError("The " + value + " is not a directoy.")
        else:
            if (not os.path.isfile(value)):
                error = IOError("The " + value + " is not a file.")

        return error