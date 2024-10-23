from .Creature import Creature


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
