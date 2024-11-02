import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import random

from Project.Element.Elements import *


# Element
def test_initialisation_element():
    o = Equipment("sword", "T")
    assert o._name == "sword"
    assert o._abbrv == "T"
    assert str(o) == "T"

    o = Equipment("gold")
    assert o._name == "gold"
    assert o._abbrv == "g"
    assert str(o) == "g"


def test_description():
    assert Element("sword").description() == "<sword>"
    assert Element("Gold").description() == "<Gold>"


def test_meet():
    hero = Hero()
    o = Element("Gold")
    assert o.meet(hero) == True
    assert hero.description() == "<Hero>(10)[G]"
    assert (o in hero._inventory) == True


# Equipment
def test_heritage():
    assert isinstance(Equipment("Sword"), Element) == True
    assert isinstance(Creature("Goblin", 5), Element) == True
    assert isinstance(Hero(), Element) == True
    assert isinstance(Creature("Goblin", 5), Equipment) == False
    assert isinstance(Element("XXX"), Equipment) == False


def test_meet():
    h = Hero()
    assert h.description() == "<Hero>(10)[]"
    o = Equipment("Golf")
    o.meet(h)
    assert h.description() == "<Hero>(10)[G]"
    assert (o in h._inventory) == True


# Creature
def test_initialisation_creature():
    o = Creature("Goblin", 10)
    assert o._name == "Goblin"
    assert o._abbrv == "G"
    assert o._hp == 10
    assert o._strength == 1

    em = Creature("Evil Mushroom", 15, "M", 3)
    assert em._name == "Evil Mushroom"
    assert em._abbrv == "M"
    assert em._hp == 15
    assert em._strength == 3


def test_heritage():
    assert isinstance(Creature("Goblin", 5), Element) == True


def test_description():
    assert Creature("Goblin", 9).description() == "<Goblin>(9)"
    assert Creature("Snake", 2).description() == "<Snake>(2)"


def test_meet():
    h = Hero()
    o = Creature("Ork", 3)
    assert o.meet(h) == False
    assert h.description() == "<Hero>(10)[]"
    assert o.description() == "<Ork>(1)"
    assert o.meet(h) == True
    assert h.description() == "<Hero>(10)[]"
    assert o.description() == "<Ork>(-1)"

    h = Hero(_hp=3, _strength=10)
    o = Creature(_name="Ork", _strength=10, _hp=12)
    assert o.meet(h) == False
    assert h.description() == "<Hero>(3)[]"
    assert o.description() == "<Ork>(2)"


# Hero
def test_initialisation_hero():
    h = Hero()
    assert h._name == "Hero"
    assert h._abbrv == "@"
    assert h._hp == 10
    assert h._strength == 2
    assert h._inventory == []


def test_take():
    h = Hero()
    s = Equipment("sword")
    h.take(s)
    assert h._inventory == [s]
    assert h.description() == "<Hero>(10)[s]"


def test_description():
    h = Hero()
    assert h.description() == "<Hero>(10)[]"


# Game
def test_initialisation():
    assert str(Game()._hero) == "@"
    assert Game()._level == 1
    assert Game()._floor == None
    assert Game()._message == []
    assert Game(level=3)._level == 3
    assert str(Game(hero=Hero("Conan"))._hero) == "@"

    assert str(Game.equipments) == "{0: [!, o], 1: [s, b], 2: [c]}"
    assert str(Game.monsters) == "{0: [G, W], 1: [O, B], 5: [D]}"


def test_buildFloor():
    random.seed(42)
    g = Game()
    assert g._floor == None
    g.buildFloor()
    assert g._floor != None
    assert isinstance(g._floor, Map) == True


def test_messages():
    theGame().readMessages()
    Equipment("sword").meet(theGame()._hero)
    assert theGame().readMessages() == "You pick up a sword. "
    Creature("Goblin", 5).meet(theGame()._hero)
    assert theGame().readMessages() == "The Hero hits the <Goblin>(3). "
    theGame()._hero.meet(Creature("Orc", 10))
    assert theGame().readMessages() == "The Orc hits the <Hero>(9)[s]. "


def test_rand():
    assert str(Game().randElement({0: [Equipment("x")]})) == "x"

    random.seed(42)
    g = Game()
    assert g.randEquipment().description() == "<sword>"
    assert g.randEquipment().description() == "<sword>"
    assert g.randEquipment().description() == "<potion>"
    assert g.randMonster().description() == "<Ork>(6)"
    assert g.randMonster().description() == "<Goblin>(4)"
    assert g.randMonster().description() == "<Goblin>(4)"


# Map
def test_initialisation():
    h = Hero()
    map = Map(5, hero=h)
    assert map.ground == "."
    assert map.empty == " "
    assert map.dir["z"] == Coord(0, -1)
    assert map.dir["q"] == Coord(-1, 0)
    assert map.dir["s"] == Coord(0, 1)
    assert map.dir["d"] == Coord(1, 0)
    assert (h in map._elem) == True
    assert map._roomsToReach == []
    assert len(map._mat) == 5


def test_len():
    map = Map()
    assert len(map) == 20
    map = Map(3)
    assert len(map) == 3


def test_contains():
    assert (Coord(0, 4) in Map()) == True
    assert (Coord(0, 4) in Map(3)) == False
    assert (Coord(0, 5) in Map()) == True
    assert (Coord(-1, 3) in Map()) == False
    assert (Coord(1, -1) in Map()) == False
    assert (Coord(5, 2) in Map()) == True
    assert (Coord(4, 4) in Map()) == True


def test_str():
    map = Map(3)
    assert str(map) == "...\n.@.\n...\n"


def test_findRoom():
    m = Map(7)
    m.addRoom(Room(Coord(0, 0), Coord(2, 2)))
    m.addRoom(Room(Coord(2, 3), Coord(6, 6)))
    assert str(m.findRoom(Coord(1, 1))) == "[<0,0>,<2,2>]"
    assert str(m.findRoom(Coord(1, 5))) == "False"
    assert str(m.findRoom(Coord(2, 2))) == "[<0,0>,<2,2>]"
    assert str(m.findRoom(Coord(2, 3))) == "[<2,3>,<6,6>]"
    assert str(m.findRoom(Coord(4, 5))) == "[<2,3>,<6,6>]"
    assert str(m.findRoom(Coord(5, 1))) == "False"


def test_intersectNone():
    m = Map(7)
    m.addRoom(Room(Coord(0, 0), Coord(2, 2)))
    m.addRoom(Room(Coord(2, 3), Coord(6, 6)))
    assert m.intersectNone(Room(Coord(1, 0), Coord(1, 5))) == False
    assert m.intersectNone(Room(Coord(0, 3), Coord(1, 5))) == True
    assert m.intersectNone(Room(Coord(1, 1), Coord(4, 4))) == False
    assert m.intersectNone(Room(Coord(1, 3), Coord(5, 6))) == False
    assert m.intersectNone(Room(Coord(0, 4), Coord(1, 5))) == True


def test_move():
    h = Hero()
    m = Map(3, hero=h)
    m.put(Coord(0, 2), Equipment("Sword"))
    assert str(m) == "...\n.@.\nS..\n"
    assert m._hero.description() == "<Hero>(10)[]"
    m.move(m._hero, Coord(0, 1))
    assert str(m) == "...\n...\nS@.\n"
    assert m._hero.description() == "<Hero>(10)[]"
    assert str(m._elem) == "{S: <0,2>, @: <1,2>}"
    m.move(m._hero, Coord(-1, 0))
    assert m._hero.description() == "<Hero>(10)[S]"
    assert m._elem == {h: Coord(1, 2)}


def test_map():
    h = Hero()
    m = Map(3, hero=h)
    assert m._hero.description() == "<Hero>(10)[]"
    assert m._elem[m._hero] == Coord(1, 1)


def test_raise_get():
    try:
        Map().get(42)
        assert True == False
    except TypeError:
        print("Test passed")
        assert True == True

    try:
        Map().get(Coord(-1, 0))
        assert True == False
    except IndexError:
        print("Test passed")
        assert True == True


def test_raise_put():
    m = Map()
    try:
        m.put(42, Hero())
        assert True == False
    except TypeError:
        print("Test passed")
        assert True == True

    try:
        m.put(Coord(-1, 0), Hero())
        assert True == False
    except IndexError:
        print("Test passed")
        assert True == True

    try:
        m.put(Coord(1, 1), "@")
        assert True == False
    except TypeError:
        print("Test passed")
        assert True == True

    try:
        m.put(Coord(1, 1), Hero())
        m.put(Coord(1, 1), Hero())
        assert True == False
    except ValueError:
        print("Test passed")
        assert True == True


def test_check():
    m = Map()
    try:
        m.checkCoord(Coord(-1, 0))
        assert True == False
    except IndexError:
        print("Test passed")
        assert True == True

    try:
        m.checkCoord(42)
        assert True == False
    except TypeError:
        print("Test passed")
        assert True == True

    try:
        m.checkElement(42)
        assert True == False
    except TypeError:
        print("Test passed")
        assert True == True


# Room


def test_str():
    r1 = Room(Coord(2, 3), Coord(4, 5))
    assert str(r1._c1) == "<2,3>"
    assert str(r1._c2) == "<4,5>"
    assert str(r1) == "[<2,3>,<4,5>]"


def test_contains():
    r1 = Room(Coord(2, 3), Coord(4, 5))
    assert (Coord(0, 1) in r1) == False
    assert (Coord(2, 1) in r1) == False
    assert (Coord(2, 3) in r1) == True
    assert (Coord(4, 4) in r1) == True
    assert (Coord(3, 4) in r1) == True
    assert (Coord(4, 5) in r1) == True
    assert (Coord(4, 6) in r1) == False
    assert (Coord(5, 6) in r1) == False


def test_center():
    assert Room(Coord(0, 0), Coord(4, 5)).center() == Coord(2, 2)
    assert Room(Coord(2, 7), Coord(8, 9)).center() == Coord(5, 8)
    assert Room(Coord(2, 5), Coord(7, 8)).center() == Coord(4, 6)


def test_intersect():
    r = Room(Coord(5, 4), Coord(8, 9))
    assert r.intersect(Room(Coord(0, 1), Coord(3, 2))) == False
    assert r.intersect(Room(Coord(1, 2), Coord(10, 10))) == True
    assert r.intersect(Room(Coord(8, 2), Coord(9, 12))) == True


def test_randCoord():
    random.seed(22)
    assert Room(Coord(0, 3), Coord(7, 6)).randCoord() == Coord(2, 4)
    assert Room(Coord(10, 13), Coord(47, 56)).randCoord() == Coord(11, 52)


def test_randEmptyCoord():
    m = Map(3)
    m.rm(Coord(1, 1))
    m.put(Coord(2, 1), Equipment("x"))
    m.put(Coord(0, 2), Equipment("x"))
    random.seed(0)
    assert m._rooms[0].randEmptyCoord(m) == Coord(0, 1)
    assert m._rooms[0].randEmptyCoord(m) == Coord(2, 0)
    assert m._rooms[0].randEmptyCoord(m) == Coord(2, 0)
    assert m._rooms[0].randEmptyCoord(m) == Coord(1, 0)


def test_decorate():
    random.seed(1)
    m = Map(20)
    print(m)
    m._rooms[0].decorate(m)
    m._rooms[1].decorate(m)
    print(m)
    print(m._elem)
