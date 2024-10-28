import random
from typing import Dict, List, Union

from Project.Element.Elements import Element, Hero

from .Coord import Coord
from .Room import Room


class Map:
    empty = " "
    ground = "."
    dir = {"z": Coord(0, -1), "q": Coord(-1, 0), "s": Coord(0, 1), "d": Coord(1, 0)}

    def __init__(
        self,
        size: int = 20,
        hero: Hero = Hero(),
        nbrooms: int = 7,
    ) -> None:
        self._size = size
        self._hero = hero
        self._mat = [[Map.empty for _ in range(size)] for _ in range(size)]
        self._elem: Dict[Element, Coord] = {}
        self._roomsToReach: List[Room] = []
        self._rooms: List[Room] = []
        self.generateRooms(nbrooms)
        self.reachAllRooms()
        self.put(self._rooms[0].center(), hero)

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
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def get_pos(self, e: Element) -> Coord:
        self.checkElement(e)
        return self._elem[e]

    def put(self, c: Coord, e: Element) -> None:
        self.checkCoord(c)
        self.checkElement(e)
        if self._mat[c.y][c.x] != Map.ground:
            print(self)
            print("cell: ", self._mat[c.y][c.x])
            raise ValueError("Incorect cell")
        if e in self._elem:
            raise KeyError("Already placed")

        self._mat[c.y][c.x] = e
        self._elem[e] = c

    def rm(self, c: Coord) -> None:
        self.checkCoord(c)
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

    def reach(self) -> None:
        roomA: Room = random.choice(self._rooms)
        roomB: Room = random.choice(self._roomsToReach)
        self.corridor(roomA.center(), roomB.center())

    def reachAllRooms(self) -> None:
        self._rooms.append(self._roomsToReach.pop())
        while self._roomsToReach != []:
            self.reach()

    def randRoom(self) -> Room:
        x1: int = random.randint(0, len(self) - 3)
        y1: int = random.randint(0, len(self) - 3)
        height: int = random.randint(3, 9)
        width: int = random.randint(3, 9)
        x2: int = min(len(self) - 1, x1 + width)
        y2: int = min(len(self) - 1, y1 + height)
        return Room(Coord(x1, y1), Coord(x2, y2))

    def generateRooms(self, n: int) -> None:
        for _ in range(n):
            r: Room = self.randRoom()
            if self.intersectNone(r):
                self.addRoom(r)

    def move(self, e: Element, way: Coord) -> None:
        c2 = self.get_pos(e) + way
        if c2 not in self:
            return
        if self.get(c2) == Map.empty:
            return
        if c2 in self and self.get(c2) == Map.ground:
            self.rm(self.get_pos(e))
            self.put(c2, e)
        else:
            if c2 in self and self.get(c2).meet(e) == True:
                self.rm(c2)

    def checkCoord(self, c: Coord) -> None:
        if not (isinstance(c, Coord)):
            raise TypeError("Not a Coord")
        if c.x < 0 or c.y < 0 or c.x > len(self) or c.y > len(self):
            raise IndexError("Out of map Coord")

    def checkElement(self, e) -> None:
        if not (isinstance(e, Element)):
            raise TypeError("Not an Element")

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
