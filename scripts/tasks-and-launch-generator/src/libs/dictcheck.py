from .validatable import Validatable
from .dictspec import DictSpec

class DictCheck(Validatable):
    def __init__(self, specs):
        # type: (list[DictSpec]) -> DictCheck
        self.specs = specs

    def validate(self, d):
        if (not isinstance(d, dict)):
            return TypeError("The value is not a dict.")

        errors = [] # type: list[Exception]
        for spec in self.specs:
            value = d.get(spec.key.name)
            if value is None:
                if not spec.key.optional:
                    errors.append(KeyError("The " + spec.key.name + " not found."))
                continue

            error = spec.value.validatable.validate(value)
            if (error is not None):
                errors.append(error)

        if (len(errors) > 0):
            error_messages = [];
            for e in errors:
                error_messages.append(str(e))
            return ValueError("\n" + "\n".join(error_messages))
        else:
            return