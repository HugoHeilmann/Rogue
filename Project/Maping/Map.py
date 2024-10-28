from typing import Union

from Project.Element.Elements import *

from .Coord import Coord
from .Room import Room


class Map:
    empty = " "
    ground = "."
    dir = {"z": Coord(0, -1), "q": Coord(-1, 0), "s": Coord(0, 1), "d": Coord(1, 0)}

    def __init__(
        self, size: int = 20, pos: Coord = Coord(1, 1), hero: Hero = Hero()
    ) -> None:
        self._size = size
        self._pos = pos
        self._hero = hero
        self._mat = [[Map.empty for _ in range(size)] for _ in range(size)]
        self._elem = {}
        # self.put(pos, hero)
        self._roomsToReach = []
        self._rooms = []

    def __len__(self) -> int:
        return len(self._mat)

    def __contains__(self, item) -> bool:
        if isinstance(item, Coord):
            return 0 <= item.x < len(self) and 0 <= item.y < len(self)
        else:
            return item in self._elem

    def __repr__(self) -> str:
        matrix = ""
        for i in range(len(self._mat)):
            for j in self._mat[i]:
                matrix += str(j)
            matrix += "\n"
        return matrix

    def get(self, c: Coord):
        return self._mat[c.y][c.x]

    def get_pos(self, e: Element) -> Coord:
        return self._elem[e]

    def put(self, c: Coord, e: Element) -> None:
        self._mat[c.y][c.x] = e
        self._elem[e] = c

    def rm(self, c: Coord) -> None:
        del self._elem[self.get(c)]
        self._mat[c.y][c.x] = Map.ground

    def addRoom(self, r: Room):
        self._roomsToReach.append(r)
        for i in range(r._c1.x, r._c2.x + 1):
            for j in range(r._c1.y, r._c2.y + 1):
                self._mat[j][i] = Map.ground

    def findRoom(self, c: Coord) -> Union[Room, bool]:
        for r in self._roomsToReach:
            if c in r:
                return r
        return False

    def intersectNone(self, room: Room) -> bool:
        for r in self._roomsToReach:
            if room.intersect(r):
                return False
        return True

    def dig(self, c: Coord) -> None:
        self._mat[c.y][c.x] = Map.ground
        if self.findRoom(c) != False:
            r: Room = self.findRoom(c)
            self._roomsToReach.remove(r)
            self._rooms.append(r)

    def corridor(self, start: Coord, end: Coord) -> None:
        if start.y > end.y:
            while start.y != end.y:
                self.dig(start)
                start.y -= 1
        else:
            while start.y != end.y:
                self.dig(start)
                start.y += 1
        if start.x > end.x:
            while start.x != end.x:
                self.dig(start)
                start.x -= 1
        else:
            while start.x != end.x:
                self.dig(start)
                start.x += 1
        self.dig(end)

    def move(self, e: Element, way: Coord) -> None:
        c2 = self.get_pos(e) + way
        if c2 in self and self.get(c2) == Map.ground:
            self.rm(self.get_pos(e))
            self.put(c2, e)
        else:
            if c2 in self and self.get(c2).meet(e) == True:
                self.rm(c2)

    def play(self):
        print("--- Welcome Hero! ---")
        while self._hero._hp > 0:
            print()
            print(self)
            print(self._hero.description())
            self.move(self._hero, Map.dir[getch()])
        print("--- Game Over ---")


def getch():
    try:
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        import msvcrt

        return msvcrt.getch().decode("utf-8")
