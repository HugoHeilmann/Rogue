from typing import List

from Project.Element.Elements import Hero
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
    def __init__(self, hero: Hero = None, level: int = 1, floor: Map = None) -> None:
        object.__init__(self, hero, level, floor)
