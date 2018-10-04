class OverrideRootError(Exception):
    def __init__(self):
        super().__init__(self, "Cannot override Tree root node")

class TreeHeightError(Exception):
    def __init__(self):
        super().__init__(self, "Cannot add node lower than tree height")
