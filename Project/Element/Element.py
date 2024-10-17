class Element:
    def __init__(self, _name: str, _abbrv: str = ""):
        self._name = _name
        self._abbrv = _abbrv
        if self._abbrv == "":
            self._abbrv = self._name[0]

    def __repr__(self) -> str:
        return self._abbrv

    def description(self) -> str:
        return f"<{self._name}>"
