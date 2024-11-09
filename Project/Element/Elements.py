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


def heal(creature: "Creature", power: int = 3) -> bool:
    creature._hp += power
    return True


def manaHeal(hero: "Hero", power: int = 3) -> bool:
    hero._mana += power
    return True


def hyperBeam(hero: "Hero", power: int) -> bool:
    direction: Coord = theGame().selectCoord(Map.dir_arrow)
    location = theGame()._floor.pos(hero) + direction
    while location in theGame()._floor and theGame()._floor.get(location) != Map.empty:
        c = theGame()._floor.get(location)
        if isinstance(c, Creature):
            c._hp -= power
            theGame().addMessage("\nThe <final spark> hits the " + c.description())
            if c._hp <= 0:
                theGame()._floor.rm(location)
        location += direction
    return True


def glacialStorm(hero: "Hero", power: int) -> bool:
    position: Coord = theGame()._floor.pos(hero)

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            new_pos: Coord = Coord(position.x + dx, position.y + dy)
            c = theGame()._floor.get(new_pos)
            if (
                new_pos in theGame()._floor
                and isinstance(c, Creature)
                and not isinstance(c, Hero)
            ):
                c._hp -= power
                theGame().addMessage(
                    "\nThe <glacial storm> hits the " + c.description()
                )
                if c._hp <= 0:
                    theGame()._floor.rm(new_pos)
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
        return super().description() + f"({self._usefullPower})"

    def meet(self, hero: "Hero") -> bool:
        theGame().addMessage("\nYou pick up a " + str(self._name))
        hero.take(self)
        return True

    def use(self, creature: "Creature"):
        if self.usage != None:
            theGame().addMessage(
                "\nThe " + str(creature._name) + " uses the " + str(self._name)
            )
            if self._requipable != "" and isinstance(creature, Hero):
                creature.requipment(self)
                return True
            else:
                return self.usage(creature)
        else:
            theGame().addMessage("\nThe " + str(self._name) + " is not usable")
            return False


class Spell:
    def __init__(self, name: str, cost: int = 1, power: int = 3, usage=None):
        self._name = name
        self._cost = cost
        self._power = power
        self.usage = usage

    def description(self) -> str:
        return f"<{self._name}>({self._cost})[{self._power}]"

    def use(self, hero: "Hero"):
        if self.usage != None:
            if hero._mana >= self._cost:
                theGame().addMessage("\nYou use the spell " + self.description())
                hero._mana -= self._cost
                return self.usage(hero, self._power)
            else:
                theGame().addMessage(
                    "\nYou don't have enough mana to use the spell "
                    + self.description()
                )
                return False
        else:
            theGame().addMessage("\nThe spell " + self._name + " is not usable")
            return False


class Requip:
    def __init__(
        self,
        helmet: Equipment = None,
        armor: Equipment = None,
        shoes: Equipment = None,
        weapon: Equipment = None,
    ):
        self._requip = {
            "helmet": helmet,
            "armor": armor,
            "shoes": shoes,
            "weapon": weapon,
        }

    def add(self, item: Equipment) -> None:
        if self._requip[item._requipable] != None:
            print("You've already requipped <" + item._requipable + ">")
            print(
                "Do you want to replace "
                + self._requip[item._requipable].description()
                + " for "
                + item.description()
                + " ? y/n"
            )
            c: str = getch()
            if c == "y":
                theGame().addMessage(
                    f"\nYou've requiped {item.description()} instead of {self._requip[item._requipable].description()}"
                )
                self._requip[item._requipable] = item
        else:
            self._requip[item._requipable] = item
            theGame().addMessage(f"\nYou've requiped {item.description()}")


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
            "\nThe " + str(other._name) + " hits the " + str(self.description())
        )
        return self._hp <= 0


class Archery(Creature):
    def __init__(
        self,
        name: str,
        hp: int,
        abbrv: str = "",
        strength: int = 1,
        defense: int = 0,
        speed: int = 1,
    ) -> None:
        Creature.__init__(self, name, hp, abbrv, strength, defense, speed)

    def throw(self) -> None:
        direction: Coord = Coord.direction(
            theGame()._floor.pos(self), theGame()._floor.pos(theGame()._hero)
        )
        location = theGame()._floor.pos(self) + direction
        while (
            location in theGame()._floor
            and theGame()._floor.get(location) == Map.ground
        ):
            location += direction
        if location in theGame()._floor and isinstance(
            theGame()._floor.get(location), Hero
        ):
            theGame()._hero.meet(self)


class Hero(Creature):
    def __init__(
        self,
        name: str = "Hero",
        hp: int = 10,
        abbrv: str = "@",
        strength: int = 2,
        defense: int = 0,
        speed: int = 1,
        mana: int = 5,
        requip: Requip = Requip(),
    ) -> None:
        Creature.__init__(self, name, hp, abbrv, strength, defense, speed)
        self._mana = mana
        self._requipment = requip
        self._inventory = []

    def description(self) -> str:
        return (
            Creature.description(self)
            + "{"
            + str(self._mana)
            + "}"
            + str(self._inventory)
        )

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
        res += "> mana : " + str(dict["_mana"]) + "\n"
        res += "> REQUIPMENTS : "
        for piece, equipment in self._requipment._requip.items():
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

    def throw(self) -> None:
        item: Equipment = theGame().select(self._inventory)
        direction: Coord = theGame().selectCoord(Map.dir_arrow)
        location = theGame()._floor.pos(self) + direction
        while (
            location in theGame()._floor
            and theGame()._floor.get(location) == Map.ground
        ):
            location += direction
        if location in theGame()._floor and isinstance(
            theGame()._floor.get(location), Creature
        ):
            dead: bool = theGame()._floor.get(location).meet(item)
            if dead:
                theGame()._floor.rm(location)
        if not item._thrower:
            self._inventory.remove(item)

    def requipment(self, item: Equipment) -> None:
        item.usage(self)
        self._requipment.add(item)

    def cast(self) -> None:
        l: List[Spell] = []
        for i in range(3):  # A changer par rapport au niveau du héros
            l += theGame().spells[i]
        spell: Spell = theGame().select(l)
        spell.use(self)

    def toss(self) -> None:
        item = theGame().select(self._inventory)
        if item in self._inventory:
            self._inventory.remove(item)
            theGame().addMessage(f"\nYou've tossed <{item._name}>")


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

    def reduced(self) -> str:
        s = ""
        heroCoord: Coord = self.pos(self._hero)
        x: int = 0
        for i in self._mat:
            y: int = 0
            for j in i:
                if Coord.distance(heroCoord, Coord(y, x)) < 5:
                    s += str(j)
                else:
                    s += self.empty
                y += 1
            s += "\n"
            x += 1
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
            if isinstance(elem, Creature) and type(elem) != Hero:
                for _ in range(elem._speed):
                    badGuy: Coord = self.pos(elem)
                    if Coord.distance(badGuy, target) <= 4 and type(elem) == Archery:
                        elem.throw()
                    elif Coord.distance(badGuy, target) <= 6:
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
            Equipment("potion", "!", usage=lambda hero: manaHeal(hero)),
            Equipment("gold", "o"),
        ],
        1: [
            Equipment(
                "sword",
                usage=lambda creature: setStrength(creature, creature._strength + 1),
                requipable="weapon",
            ),
            Equipment("light bow", "b", thrower=True),
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
                requipable="shoes",
            ),
        ],
    }

    monsters = {
        0: [Creature("Goblin", 4), Creature("Bat", 2, "W"), Archery("Archer", 6)],
        1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)],
        5: [Creature("Dragon", 20, strength=3)],
    }

    spells = {
        0: [
            Spell(
                "Heal",
                cost=1,
                power=3,
                usage=lambda creature, power: heal(creature, power),
            ),
            Spell(
                "Teleport",
                cost=1,
                power=None,
                usage=lambda creature, power: teleport(creature, False),
            ),
        ],
        1: [
            Spell(
                "Glacial Storm",
                cost=2,
                power=3,
                usage=lambda creature, power: glacialStorm(creature, power),
            )
        ],
        2: [
            Spell(
                "Final Spark",
                cost=3,
                power=5,
                usage=lambda creature, power: hyperBeam(creature, power),
            )
        ],
        5: [],
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
        # Lancer un sort
        "m": lambda hero: hero.cast(),
        # Pas d'action
        "x": lambda hero: None,
        # Description complète
        "i": lambda hero: theGame().addMessage("\n" + hero.fullDescrition()),
        # Suicide
        "k": lambda hero: hero.__setattr__("_hp", 0),
        # Utiliser un objet
        "u": lambda hero: hero.use(theGame().select(hero._inventory)),
        # Jeter un objet
        "t": lambda hero: hero.toss(),
        # Montrer le lexique des actions
        "l": lambda hero: theGame().showActions(),
    }

    def __init__(self, hero: Hero = Hero(), level: int = 1):
        self._hero = hero
        self._level = level
        self._floor = None
        self._message: List[str] = []

    def showActions(self) -> None:
        res: str = ""
        res += "\n<-- ACTIONS -->\n"
        res += "\n> MOVES : \n"
        res += "Lateral : z(↑), q(←), s(↓), d(→)\n"
        res += "Diagonal : a(↖), e(↗), w(↙), c(↘)\n"
        res += "\n> OBJECTS : \n"
        res += "Use : u, then choose object\n"
        res += "Toss : t, then choose object\n"
        res += "\n> ATTACKS : \n"
        res += "Throw an object against someone : j, then choose object, then choose direction\n"
        res += "Cast a spell : m, then choose a spell\n"
        res += "\n> GESTION : \n"
        res += "Full description of yourself : i\n"
        res += "Kill yourself : k\n"
        res += "Show this lexical : l\n"
        res += "Do nothing : every other letter\n"
        theGame().addMessage(res)

    def buildFloor(self) -> Map:
        self._floor = Map(hero=self._hero)
        theGame()._floor = self._floor
        stairs = Room.center(theGame()._floor._rooms[-1])
        theGame()._floor.put(stairs, Stairs())
        return self._floor

    def buildEndFloor(self) -> Map:
        self._floor = Map(hero=self._hero)
        theGame()._floor = self._floor
        masterSword = Room.center(theGame()._floor._rooms[-1])
        theGame()._floor.put(masterSword, MasterSword())
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
        print(
            "\n----------------------------- Welcome Hero! -----------------------------"
        )
        print(
            "\nYour objective is to find the legendary Master Sword hidden in the dungeon"
        )
        print("However, the monsters are here to keep you from touching it")
        print("Use the character l to see your potential of actions")
        print("Don't worry, monsters won't approch you while you read the lexical ;)")
        print("Use the character c to begin your adventure !")
        continu: bool = False
        while not continu:
            c = getch()
            if c == "c":
                continu = True
        while self._hero._hp > 0:
            for _ in range(self._floor._hero._speed):
                os.system("cls")
                print("Level -" + str(self._level))
                print()
                print(self._floor.reduced())
                print(self._hero.description())
                print(self.readMessages())
                c = getch()
                if c in Game._actions:
                    Game._actions[c](self._hero)
                    if c == "k" or c == "l":
                        break
                self._floor.moveAllMonsters()
        print(self.readMessages())
        print("--- Game Over ---")


class Stairs(Element):
    def __init__(self, name="Stairs", abbrv="E") -> None:
        Element.__init__(self, name, abbrv)

    def meet(self, hero: Hero) -> bool:
        theGame().addMessage(f"\n{hero._name} goes down")
        theGame()._level += 1
        if theGame()._level == 5:
            theGame().buildEndFloor()
        else:
            theGame().buildFloor()
        return True


class MasterSword(Element):
    def __init__(self, name="Master Sword", abbrv="⚔") -> None:
        Element.__init__(self, name, abbrv)

    def meet(self, hero: Hero) -> None:
        import sys

        print("Congratulation Hero, you've retrieved the legendary Master Sword !")
        print("\n--- You won ! ---")
        sys.exit()


def theGame(game=Game()):
    return game


import msvcrt


def getch():
    return msvcrt.getch().decode("utf-8")
