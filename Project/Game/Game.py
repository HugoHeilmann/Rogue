import math
import random
from typing import Dict, List, Union

from Project.Element.Elements import Creature, Equipment, Hero
from Project.Maping.Map import Map


class object:
    def __init__(self, hero: Hero = None, level: int = 1, floor: Map = None) -> None:
        if hero == None:
            self._hero: Hero = Hero()
        else:
            self._hero: Hero = hero
        self._level: int = level
        self._floor: Map = floor
        self._message: List[str] = []


class Game(object):
    equipments = {
        0: [Equipment("potion", "!"), Equipment("gold", "o")],
        1: [Equipment("sword"), Equipment("bow")],
        2: [Equipment("chainmail")],
    }
    monsters = {
        0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
        1: [Creature("Ork", 6, _strength=2), Creature("Blob", 10)],
        5: [Creature("Dragon", 20, _strength=3)],
    }

    def __init__(self, hero: Hero = None, level: int = 1, floor: Map = None) -> None:
        object.__init__(self, hero, level, floor)

    def buildFloor(self) -> Map:
        self._floor = Map(hero=self._hero)
        return self._floor

    def addMessage(self, msg: str) -> None:
        self._message.append(msg)

    def readMessages(self) -> str:
        res: str = ""
        for msg in self._message:
            res += msg
            res += ". "
        self._message = []
        return res

    def randElement(
        self, collection: Dict[int, List[Union[Equipment, Creature]]]
    ) -> Union[Equipment, Creature]:
        x: int = math.floor(random.expovariate(1 / self._level))
        while x not in self.monsters.keys():
            x -= 1
        for rarity in collection:
            if rarity == x:
                elements = collection[rarity]
        return random.choice(elements)

    def randEquipment(self) -> Equipment:
        return self.randElement(self.equipments)

    def randMonster(self) -> Creature:
        return self.randElement(self.monsters)


def theGame(game=Game()):
    return game
