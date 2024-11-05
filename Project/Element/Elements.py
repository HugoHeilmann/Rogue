import abc
import copy
import random
from typing import Dict, List, Union

from Maping.Coord import Coord


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


def heal(creature: "Creature") -> bool:
    creature._hp += 3
    return True


def teleport(creature: "Creature", unique):
    start = theGame()._floor.pos(creature)
    room = random.choice(theGame()._floor._rooms)
    arrival = room.randEmptyCoord(theGame()._floor)
    theGame()._floor._mat[start.y][start.x] = Map.ground
    theGame()._floor._mat[arrival.y][arrival.x] = creature
    theGame()._floor._elem[creature] = arrival
    return unique


def setStrength(creature: "Creature", strength: int) -> bool:
    creature._strength = strength
    return True


def setDefense(creature: "Creature", defense: int):
    creature._defense = defense


def setSpeed(creature: "Creature", speed: int):
    creature._speed = speed


class Equipment(Element):
    def __init__(
        self,
        name: str,
        abbrv: str = "",
        usage=None,
        strength: int = 1,
        usefullPower: int = 1,
        thrower: bool = False,
        requipable: str = "",
    ) -> None:
        Element.__init__(self, name, abbrv)
        self.usage = usage
        self._strength = strength
        self._usefullPower = usefullPower
        self._thrower = thrower
        self._requipable = requipable

    def description(self) -> str:
        return super().description() + f"({self._power})"

    def meet(self, hero: "Hero") -> bool:
        theGame().addMessage("You pick up a " + str(self._name))
        hero.take(self)
        return True

    def use(self, creature: "Creature"):
        if self.usage != None:
            theGame().addMessage(
                "The " + str(creature._name) + " uses the " + str(self._name)
            )
            if self._requipable != "" and isinstance(creature, Hero):
                creature.requipment(self)
                return True
            else:
                return self.usage(creature)
        else:
            theGame().addMessage("The " + str(self._name) + " is not usable")
            return False


class Requip:
    def __init__(
        self,
        helmet: Equipment = None,
        armor: Equipment = None,
        shoes: Equipment = None,
        weapon: Equipment = None,
    ):
        self._helmet = helmet
        self._armor = armor
        self._shoes = shoes
        self._weapon = weapon

    def getAll(self) -> Dict[str, Equipment]:
        return {
            "helmet": self._helmet,
            "armor": self._armor,
            "shoes": self._shoes,
            "weapon": self._weapon,
        }

    def add(self, item: Equipment) -> None:
        part: str = item._requipable
        if part == "helmet":
            self._helmet = item
        elif part == "armor":
            self._armor = item
        elif part == "shoes":
            self._shoes = item
        elif part == "weapon":
            self._weapon = item
        theGame().addMessage(f"You've requiped {item.description()}")


class Creature(Element):
    def __init__(
        self,
        name: str,
        hp: int,
        abbrv: str = "",
        strength: int = 1,
        defense: int = 0,
        speed: int = 1,
    ) -> None:
        Element.__init__(self, name, abbrv)
        self._hp = hp
        self._strength = strength
        self._defense = defense
        self._speed = speed

    def description(self) -> str:
        return Element.description(self) + "(" + str(self._hp) + ")"

    def meet(self, other: "Creature") -> bool:
        damageMin: int = 1
        damageCalculate: int = other._strength - self._defense
        self._hp -= max(damageMin, damageCalculate)
        theGame().addMessage(
            "The " + str(other._name) + " hits the " + str(self.description())
        )
        return self._hp <= 0


class Hero(Creature):
    def __init__(
        self,
        name: str = "Hero",
        hp: int = 10,
        abbrv: str = "@",
        strength: int = 2,
        defense: int = 0,
        speed: int = 1,
        requip: Requip = Requip(),
    ) -> None:
        Creature.__init__(self, name, hp, abbrv, strength, defense, speed)
        self._requip = requip
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
        res += "> defense : " + str(dict["_defense"]) + "\n"
        res += "> speed : " + str(dict["_speed"]) + "\n"
        res += "> REQUIPMENTS : "
        for piece, equipment in self._requip.getAll().items():
            if equipment != None:
                res += f"{piece} -> {equipment.description()}, "
        res += "\n> INVENTORY : " + str([item._name for item in self._inventory])
        return res

    def take(self, elem: Equipment) -> None:
        self._inventory.append(elem)
        if not isinstance(elem, Equipment):
            raise TypeError("Not in equipment")

    def use(self, item: Equipment):
        if not isinstance(item, Equipment):
            raise TypeError("Not an equipment")
        if item not in self._inventory:
            raise ValueError("Not in inventory")
        if Equipment.use(item, self):
            self._inventory.remove(item)

    def throw(self) -> bool:
        item: Equipment = theGame().select(self._inventory)
        direction: Coord = theGame().selectCoord(Map.dir_arrow)
        location = theGame()._floor.pos(self) + direction
        while theGame()._floor.get(location) == Map.ground:
            location += direction
        if isinstance(theGame()._floor.get(location), Creature):
            dead: bool = theGame()._floor.get(location).meet(item)
            if dead:
                theGame()._floor.rm(location)
        if not item._thrower:
            self._inventory.remove(item)
        return isinstance(theGame()._floor.get(location), Creature)

    def requipment(self, item: Equipment) -> None:
        item.usage(self)
        self._requip.add(item)

    def toss(self) -> None:
        item = theGame().select(self._inventory)
        self._inventory.remove(item)
        theGame().addMessage(f"You've tossed <{item._name}>")


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
    dir = {
        "z": Coord(0, -1),
        "s": Coord(0, 1),
        "d": Coord(1, 0),
        "q": Coord(-1, 0),
        "a": Coord(-1, -1),
        "e": Coord(1, -1),
        "w": Coord(-1, 1),
        "c": Coord(1, 1),
    }
    dir_arrow = {
        "z": "↑",
        "s": "↓",
        "d": "→",
        "q": "←",
        "a": "↖",
        "e": "↗",
        "w": "↙",
        "c": "↘",
    }

    def __init__(self, size: int = 20, hero: Hero = Hero(), nbrooms: int = 7) -> None:
        self._mat = []
        self._rooms: List[Room] = []
        self._roomsToReach: List[Room] = []
        self._elem: Dict[Element, Coord] = {}
        self._hero = hero
        for _ in range(size):
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
        if not isinstance(c, Coord):
            raise TypeError("Not a Coord")
        if c not in self:
            raise IndexError("Out of map coord")

    def checkElement(self, o) -> Union[None, TypeError]:
        if not isinstance(o, Element):
            raise TypeError("Not a Element")

    def moveAllMonsters(self) -> None:
        target: Coord = self.pos(self._hero)
        for elem in self._elem:
            if type(elem) == Creature:
                for _ in range(elem._speed):
                    badGuy: Coord = self.pos(elem)
                    if Coord.distance(badGuy, target) <= 6:
                        c: Coord = Coord.direction(badGuy, target)
                        if (
                            self.get(self.pos(elem) + c) == self.ground
                            or self.get(self.pos(elem) + c) == self._hero
                        ):
                            self.move(elem, Coord.direction(badGuy, target))


class Game:
    equipments = {
        0: [
            Equipment("potion", "!", usage=lambda creature: heal(creature)),
            Equipment("gold", "o"),
        ],
        1: [
            Equipment(
                "sword",
                usage=lambda creature: setStrength(creature, creature._strength + 1),
                requipable="weapon",
            ),
            Equipment("bow", thrower=True),
            Equipment("potion", "!", usage=lambda creature: teleport(creature, True)),
        ],
        2: [
            Equipment(
                "chainmail",
                usage=lambda creature: setDefense(creature, creature._defense + 1),
                requipable="armor",
            ),
            Equipment(
                "iron helmet",
                "h",
                usage=lambda creature: setDefense(creature, creature._defense + 1),
                requipable="helmet",
            ),
            Equipment(
                "spike shoes",
                "k",
                usage=lambda creature: setStrength(creature, creature._strength + 1),
                requipable="shoes",
            ),
        ],
        3: [
            Equipment(
                "portoloin", "w", usage=lambda creature: teleport(creature, False)
            ),
            Equipment(
                "nimbus 2000",
                "→",
                usage=lambda creature: setSpeed(creature, creature._speed + 1),
            ),
        ],
    }

    monsters = {
        0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
        1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)],
        5: [Creature("Dragon", 20, strength=3)],
    }
    _actions = {
        # Déplacements diagonaux
        "a": lambda hero: theGame()._floor.move(hero, Coord(-1, -1)),
        "e": lambda hero: theGame()._floor.move(hero, Coord(1, -1)),
        "w": lambda hero: theGame()._floor.move(hero, Coord(-1, 1)),
        "c": lambda hero: theGame()._floor.move(hero, Coord(1, 1)),
        # Déplacements latéraux
        "z": lambda hero: theGame()._floor.move(hero, Coord(0, -1)),
        "s": lambda hero: theGame()._floor.move(hero, Coord(0, 1)),
        "q": lambda hero: theGame()._floor.move(hero, Coord(-1, 0)),
        "d": lambda hero: theGame()._floor.move(hero, Coord(1, 0)),
        # Lancer un objet
        "j": lambda hero: hero.throw(),
        # Pas d'action
        "x": lambda hero: None,
        # Description complète
        "i": lambda hero: theGame().addMessage(hero.fullDescrition()),
        # Suicide
        "k": lambda hero: hero.__setattr__("_hp", 0),
        # Utiliser un objet
        "u": lambda hero: hero.use(theGame().select(hero._inventory)),
        # Jeter un objet
        "t": lambda hero: hero.toss(),
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

    def select(self, l: List) -> Equipment:
        print("Choose item> " + str([str(l.index(e)) + ": " + e._name for e in l]))
        c: str = getch()
        if c.isdigit() and int(c) in range(len(l)):
            return l[int(c)]
        return None

    def selectCoord(self, d: Dict) -> Coord:
        print(
            "Choose direction> "
            + str([str(i) + ": " + str(d[key]) for i, key in enumerate(d)])
        )
        c: str = getch()
        if c.isdigit() and int(c) in range(len(d)):
            key = list(d.keys())[int(c)]
            return Map.dir[key]
        return None

    def play(self) -> None:
        import os

        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self._hero._hp > 0:
            for _ in range(self._floor._hero._speed):
                os.system("cls")
                print()
                print(self._floor)
                print(self._hero.description())
                print(self.readMessages())
                c = getch()
                if c in Game._actions:
                    Game._actions[c](self._hero)
                    if c == "k":
                        break
            self._floor.moveAllMonsters()
        print(self.readMessages())
        print("--- Game Over ---")


class Stairs(Element):
    def __init__(self, name="Stairs", abbrv="E") -> None:
        Element.__init__(self, name, abbrv)

    def meet(self, hero: Hero) -> bool:
        theGame().addMessage(f"{hero._name} goes down")
        theGame().buildFloor()
        return True


def theGame(game=Game()):
    return game


import msvcrt


def getch():
    return msvcrt.getch().decode("utf-8")
