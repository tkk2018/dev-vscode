from .validatable import Validatable

class KeySpec():
    def __init__(self, name, optional=False, description=""):
        # type: (str, bool, str) -> KeySpec
        self.name = name
        self.optional = optional
        self.description = description

class ValueSpec():
    def __init__(self, value_type, validatable):
        # type: (type, Validatable) -> ValueSpec
        self.value_type = value_type
        self.validatable = validatable

class DictSpec():
    def __init__(self, key, value):
        # type: (KeySpec, ValueSpec) -> DictSpec
        self.key = key
        self.value = value