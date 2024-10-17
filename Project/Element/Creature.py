from .Element import Element


class Creature(Element):
    def __init__(self, _name: str, _hp: int, _abbrv: str = "", _strength: int = 1):
        Element.__init__(self, _name, _abbrv)
        self._hp = _hp
        self._strength = _strength

    def description(self) -> str:
        return super().description() + "(" + str(self._hp) + ")"
