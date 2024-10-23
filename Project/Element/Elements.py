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

    def meet(self, hero: "Hero") -> bool:
        hero.take(self)
        return True


class Creature(Element):
    def __init__(self, _name: str, _hp: int, _abbrv: str = "", _strength: int = 1):
        Element.__init__(self, _name, _abbrv)
        self._hp = _hp
        self._strength = _strength

    def description(self) -> str:
        return super().description() + "(" + str(self._hp) + ")"


class Hero(Creature):
    def __init__(
        self, _name: str = "Hero", _hp: int = 10, _abbrv: str = "@", _strength: int = 2
    ):
        Creature.__init__(self, _name, _hp, _abbrv, _strength)
        self._inventory = []

    def take(self, elem: object):
        self._inventory.append(elem)

    def description(self):
        return super().description() + str(self._inventory)
