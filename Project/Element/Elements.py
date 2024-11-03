import abc
import copy
import math
import random
from typing import Dict, List, Union

from ..Maping.Coord import Coord


class Element(metaclass=abc.ABCMeta):
    def __init__(self, _name: str, _abbrv: str = ""):
        self._name = _name
        self._abbrv = _abbrv
        if self._abbrv == "":
            self._abbrv = self._name[0]

    def __repr__(self) -> str:
        return self._abbrv

    def description(self) -> str:
        return f"<{self._name}>"

    @abc.abstractmethod
    def meet(self, hero: "Hero") -> bool:
        raise NotImplementedError("Abstract method")


class Equipment(Element):
    def __init__(self, name: str, abbrv: str = "") -> None:
        Element.__init__(self, name, abbrv)

    def meet(self, hero: "Hero") -> bool:
        theGame().addMessage("You pick up a " + str(self._name))
        hero.take(self)
        return True


class Creature(Element):
    def __init__(self, name: str, hp: int, abbrv: str = "", strength: int = 1) -> None:
        Element.__init__(self, name, abbrv)
        self._hp = hp
        self._strength = strength

    def description(self) -> str:
        return Element.description(self) + "(" + str(self._hp) + ")"

    def meet(self, other: "Creature") -> bool:
        self._hp -= other._strength
        theGame().addMessage(
            "The " + str(other._name) + " hits the " + str(self.description())
        )
        return self._hp <= 0


class Hero(Creature):
    def __init__(
        self, name: str = "Hero", hp: int = 10, abbrv: str = "@", strength: int = 2
    ) -> None:
        Creature.__init__(self, name, hp, abbrv, strength)
        self._inventory = []

    def description(self) -> str:
        return Creature.description(self) + str(self._inventory)

    def fullDescrition(self) -> str:
        res: str = ""
        dict = self.__dict__
        print("dict : ", dict)
        res += "> name : " + dict["_name"] + "\n"
        res += "> abbrv : " + dict["_abbrv"] + "\n"
        res += "> hp : " + str(dict["_hp"]) + "\n"
        res += "> strength : " + str(dict["_strength"]) + "\n"
        res += "> INVENTORY : " + str([item._name for item in self._inventory])
        return res

    def take(self, elem: Equipment) -> None:
        self._inventory.append(elem)
        if isinstance(elem, Equipment) == False:
            raise TypeError("Not in equipment")


class Room:
    def __init__(self, c1: Coord, c2: Coord) -> None:
        self._c1 = c1
        self._c2 = c2

    def __repr__(self) -> str:
        return "[" + str(self._c1) + ", " + str(self._c2) + "]"

    def __contains__(self, other: Coord) -> bool:
        if isinstance(other, Coord):
            return (
                min(self._c1.x, self._c2.x) <= other.x <= self._c1.x
                and min(self._c1.y, self._c2.y) <= other.y <= self._c1.y
                or min(self._c1.x, self._c2.x) <= other.x <= self._c2.x
                and min(self._c1.y, self._c2.y) <= other.y <= self._c2.y
            )

    def center(self) -> Coord:
        cx: int = (self._c1.x + self._c2.x) // 2
        cy: int = (self._c1.y + self._c2.y) // 2
        return Coord(cx, cy)

    def intersect(self, other: "Room") -> bool:
        c3s = Coord(self._c1.x, self._c2.y)
        c4s = Coord(self._c2.x, self._c1.y)
        c3o = Coord(other._c1.x, other._c2.y)
        c4o = Coord(other._c2.x, other._c1.y)
        return (
            other._c1 in self
            or other._c2 in self
            or c3o in self
            or c4o in self
            or self._c1 in other
            or self._c2 in other
            or c3s in other
            or c4s in other
        )

    def randCoord(self) -> Coord:
        rdmX = random.randint(self._c1.x, self._c2.x)
        rdmY = random.randint(self._c1.y, self._c2.y)
        return Coord(rdmX, rdmY)

    def randEmptyCoord(self, map: "Map") -> Coord:
        while True:
            res: Coord = self.randCoord()
            if map.get(res) == map.ground and res != self.center():
                return res

    def decorate(self, map: "Map") -> None:
        cea: Coord = self.randEmptyCoord(map)
        ea: Equipment = theGame().randEquipment()
        map.put(cea, ea)
        cma: Coord = self.randEmptyCoord(map)
        ma: Creature = theGame().randMonster()
        map.put(cma, ma)


class Map:
    ground = "."
    empty = " "
    dir = {"z": Coord(0, -1), "s": Coord(0, 1), "d": Coord(1, 0), "q": Coord(-1, 0)}

    def __init__(self, size: int = 20, hero: Hero = Hero(), nbrooms: int = 7) -> None:
        self._mat = []
        self._rooms: List[Room] = []
        self._roomsToReach: List[Room] = []
        self._elem: Dict[Element, Coord] = {}
        self._hero = hero
        for i in range(size):
            self._mat.append([Map.empty] * size)
        self.generateRooms(nbrooms)
        self.reachAllRooms()
        self.put(self._rooms[0].center(), self._hero)
        for room in self._rooms:
            Room.decorate(room, self)

    def __len__(self) -> int:
        return len(self._mat)

    def __contains__(self, item) -> bool:
        if isinstance(item, Coord):
            return 0 <= item.x < len(self) and 0 <= item.y < len(self)
        return item in self._elem

    def __repr__(self) -> str:
        s = ""
        for i in self._mat:
            for j in i:
                s += str(j)
            s += "\n"
        return s

    def put(self, c: Coord, o: Element) -> None:
        self.checkCoord(c)
        self.checkElement(o)
        if self._mat[c.y][c.x] != Map.ground:
            raise ValueError("Incorrect cell")
        if o in self:
            raise KeyError("Already placed")
        self._mat[c.y][c.x] = o
        self._elem[o] = c

    def get(self, c: Coord) -> Element:
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self, o: Element) -> Coord:
        self.checkElement(o)
        return self._elem[o]

    def rm(self, c: Coord) -> None:
        self.checkCoord(c)
        del self._elem[self._mat[c.y][c.x]]
        self._mat[c.y][c.x] = Map.ground

    def move(self, e: Element, way: Coord) -> None:
        orig = self.pos(e)
        dest = orig + way
        if dest in self:
            if self.get(dest) == Map.ground:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
            elif (
                self.get(dest) != Map.empty
                and self.get(dest).meet(e)
                and self.get(dest) != self._hero
            ):
                self.rm(dest)

    def addRoom(self, room: Room) -> None:
        i = 0
        while i <= room._c2.y:
            j = 0
            if room._c1.y <= i <= room._c2.y:
                while j <= room._c2.x:
                    if room._c1.x <= j <= room._c2.x:
                        self._mat[i][j] = Map.ground
                    j += 1
            i += 1
        self._roomsToReach.append(room)

    def findRoom(self, coord: Coord) -> Union[Room, bool]:
        for room in self._roomsToReach:
            if coord in room:
                return room
        return False

    def intersectNone(self, room: Room) -> bool:
        for place in self._roomsToReach:
            if place.intersect(room):
                return False
        return True

    def dig(self, coord: Coord) -> None:
        inside = self.findRoom(coord)
        if inside != False:
            self._roomsToReach.remove(inside)
            self._rooms.append(inside)
        else:
            self._mat[coord.y][coord.x] = Map.ground

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
        begin: Room = random.choice(self._rooms)
        end: Room = random.choice(self._roomsToReach)
        centA: Coord = Room.center(begin)
        centB: Coord = Room.center(end)
        self.corridor(centA, centB)

    def reachAllRooms(self) -> None:
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoom(self) -> Room:
        x1 = random.randint(0, len(self) - 3)
        y1 = random.randint(0, len(self) - 3)
        largeur = random.randint(3, 8)
        hauteur = random.randint(3, 8)
        x2 = min(len(self) - 1, x1 + largeur)
        y2 = min(len(self) - 1, y1 + hauteur)
        return Room(Coord(x1, y1), Coord(x2, y2))

    def generateRooms(self, n: int) -> None:
        for _ in range(n):
            newPlace = self.randRoom()
            if self.intersectNone(newPlace):
                self.addRoom(newPlace)

    def checkCoord(self, c) -> Union[None, TypeError, IndexError]:
        if isinstance(c, Coord) == False:
            raise TypeError("Not a Coord")
        if c not in self:
            raise IndexError("Out of map coord")

    def checkElement(self, o) -> Union[None, TypeError]:
        if not isinstance(o, Element):
            raise TypeError("Not a Element")

    def moveAllMonsters(self) -> None:
        target: Coord = self.pos(self._hero)
        for elem in self._elem:
            badGuy: Coord = self.pos(elem)
            if type(elem) == Creature and Coord.distance(badGuy, target) <= 6:
                self.move(elem, Coord.direction(badGuy, target))


class Game:
    equipments = {
        0: [Equipment("potion", "!"), Equipment("gold", "o")],
        1: [Equipment("sword"), Equipment("bow")],
        2: [Equipment("chainmail")],
    }
    monsters = {
        0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
        1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)],
        5: [Creature("Dragon", 20, strength=3)],
    }
    _actions = {
        "z": lambda hero: theGame()._floor.move(hero, Coord(0, -1)),
        "s": lambda hero: theGame()._floor.move(hero, Coord(0, 1)),
        "q": lambda hero: theGame()._floor.move(hero, Coord(-1, 0)),
        "d": lambda hero: theGame()._floor.move(hero, Coord(1, 0)),
        "i": lambda: theGame().addMessage(theGame()._hero.fullDescrition()),
        "k": lambda: theGame()._hero.__setattr__("_hp", 0),
        "": lambda: None,
    }

    def __init__(self, hero: Hero = Hero(), level: int = 1):
        self._hero = hero
        self._level = level
        self._floor = None
        self._message: List[str] = []

    def buildFloor(self) -> Map:
        self._floor = Map(hero=self._hero)
        theGame()._floor = self._floor
        stairs = Room.center(theGame()._floor._rooms[-1])
        theGame()._floor.put(stairs, Stairs())
        return self._floor

    def addMessage(self, msg: str) -> None:
        self._message.append(msg)

    def readMessages(self) -> str:
        msg: str = ""
        for message in self._message:
            msg += message
            msg += ". "
        self._message.clear()
        return msg

    def randElement(self, collection) -> Element:
        X = random.expovariate(1 / self._level)
        for i in collection:
            if i < X:
                l = collection[i]
        rdm = random.choice(l)
        return copy.copy(rdm)

    def randEquipment(self) -> Equipment:
        return self.randElement(Game.equipments)

    def randMonster(self) -> Creature:
        return self.randElement(Game.monsters)


class Stairs(Element):
    def __init__(self, name="Stairs", abbrv="E") -> None:
        Element.__init__(self, name, abbrv)

    def meet(self, hero: Hero) -> bool:
        theGame().addMessage(f"{hero._name} goes down")
        return True


def theGame(game=Game()):
    return game
