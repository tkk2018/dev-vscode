from .jsonable import Jsonable

class TaskGroup(Jsonable):
    """
    The vscode task's group.
    """

    def __init__(self, kind, isDefault):
        # type: (str, bool) -> TaskGroup
        self.kind = kind
        self.isDefault = isDefault
