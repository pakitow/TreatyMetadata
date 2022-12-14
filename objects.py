class TreatyList:
    def __init__(self, path: str = "") -> None:
        self.name = path
    @classmethod
    def setPath(cls, path: str) -> None:
        return cls(path)