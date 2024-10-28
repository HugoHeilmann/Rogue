import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import random

from Project.Element.Elements import Element, Hero
from Project.Maping.Coord import Coord
from Project.Maping.Map import Map
from Project.Maping.Room import Room

random.seed(42)


def test_initialisation():
    h = Hero()
    map = Map(5, hero=h)
    assert map.ground == "."
    assert map.empty == " "
    assert map.dir["z"] == Coord(0, -1)
    assert map.dir["q"] == Coord(-1, 0)
    assert map.dir["s"] == Coord(0, 1)
    assert map.dir["d"] == Coord(1, 0)
    assert map._elem == {h: Coord(3, 1)}
    assert str(map._rooms) == "[[<2,0>,<4,3>]]"
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


def test_get():
    map = Map(5)
    map.put(Coord(1, 1), Hero())
    assert map.get(Coord(0, 4)) == "."
    assert str(map.get(Coord(1, 1))) == "@"
    assert map.get(Coord(2, 3)) == "."


def test_pos():
    h = Hero()
    map = Map(5, hero=h)
    assert map.get_pos(h) == Coord(3, 2)
    h2 = Hero(_abbrv="X")
    map = Map(hero=h2)
    assert map.get_pos(h2) == Coord(8, 18)


def test_put():
    m = Map(5)
    m.put(Coord(3, 2), "X")
    assert str(m) == "     \n     \n...X.\n..@..\n.....\n"
    assert m._elem == {m._hero: Coord(2, 3), "X": Coord(3, 2)}


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
    m.put(Coord(0, 2), Element("Sword"))
    assert str(m) == "...\n.@.\nS..\n"
    assert m._hero.description() == "<Hero>(10)[]"
    m.move(m._hero, Coord(0, 1))
    assert str(m) == "...\n...\nS@.\n"
    assert m._hero.description() == "<Hero>(10)[]"
    assert str(m._elem) == "{S: <0,2>, @: <1,2>}"
    m.move(m._hero, Coord(-1, 0))
    assert m._hero.description() == "<Hero>(10)[S]"
    assert m._elem == {h: Coord(1, 2)}


def test_move_not_posssible():
    m = Map(5)
    assert m._elem == {m._hero: Coord(2, 2)}
    m.move(m._hero, Coord(0, -1))
    assert m._elem == {m._hero: Coord(2, 1)}
    m.move(m._hero, Coord(0, -1))
    assert m._elem == {m._hero: Coord(2, 1)}


def test_map():
    h = Hero()
    m = Map(3, hero=h)
    assert m._hero.description() == "<Hero>(10)[]"
    assert m._elem[m._hero] == Coord(1, 1)
