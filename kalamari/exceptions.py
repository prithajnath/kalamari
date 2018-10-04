class OverrideRootError(Exception):
    def __init__(self):
        super().__init__(self, "Cannot override Tree root node")
