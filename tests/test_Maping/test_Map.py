import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Elements import Element, Hero
from Project.Maping.Coord import Coord
from Project.Maping.Map import Map
from Project.Maping.Room import Room


def test_initialisation():
    map = Map(5)
    assert map.ground == "."
    assert map.empty == " "
    assert map.dir["z"] == Coord(0, -1)
    assert map.dir["q"] == Coord(-1, 0)
    assert map.dir["s"] == Coord(0, 1)
    assert map.dir["d"] == Coord(1, 0)
    assert map._elem == {}
    assert map._rooms == []
    assert map._roomsToReach == []
    assert len(map._mat) == 5
    for i in range(len(map._mat)):
        assert len(map._mat[i]) == 5

    for i in range(5):
        for j in range(5):
            assert map._mat[j][i] == Map.empty
    # assert map._elem[map._hero] == Coord(1, 1)


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
    map = Map(3, pos=Coord(0, 1))
    map.put(map._pos, Hero())
    assert str(map) == "   \n@  \n   \n"


def test_get():
    map = Map(5)
    map.put(Coord(1, 1), Hero())
    assert map.get(Coord(0, 4)) == " "
    assert str(map.get(Coord(1, 1))) == "@"
    assert map.get(Coord(2, 3)) == " "


def test_pos():
    map = Map(5, pos=Coord(1, 1))
    h = Hero()
    map.put(map._pos, h)
    assert map.get_pos(h) == Coord(1, 1)
    h2 = Hero(_abbrv="X")
    map = Map(pos=Coord(2, 3))
    map.put(map._pos, h2)
    assert map.get_pos(h2) == Coord(2, 3)


def test_put():
    m = Map(5)
    m.put(Coord(3, 2), "X")
    m.put(Coord(0, 0), "A")
    assert str(m) == "A    \n     \n   X \n     \n     \n"
    assert m._elem == {"X": Coord(3, 2), "A": Coord(0, 0)}


def test_addRoom():
    m = Map(6)
    m.addRoom(Room(Coord(1, 1), Coord(4, 3)))
    assert str(m) == "      \n .... \n .... \n .... \n      \n      \n"
    assert m._rooms == []
    assert len(m._roomsToReach) == 1
    assert str(m._roomsToReach[0]) == "[<1,1>,<4,3>]"


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


def test_dig():
    m = Map(5)
    r1 = Room(Coord(0, 0), Coord(1, 3))
    r2 = Room(Coord(3, 1), Coord(4, 4))
    m.addRoom(r1)
    m.addRoom(r2)
    assert str(m) == "..   \n.. ..\n.. ..\n.. ..\n   ..\n"
    assert m._rooms == []
    assert m._roomsToReach == [r1, r2]

    m.dig(Coord(1, 2))
    assert str(m) == "..   \n.. ..\n.. ..\n.. ..\n   ..\n"
    assert m._rooms == [r1]
    assert m._roomsToReach == [r2]

    m.dig(Coord(2, 2))
    assert str(m) == "..   \n.. ..\n.....\n.. ..\n   ..\n"
    assert m._rooms == [r1]
    assert m._roomsToReach == [r2]

    m.dig(Coord(3, 2))
    assert str(m) == "..   \n.. ..\n.....\n.. ..\n   ..\n"
    assert m._rooms == [r1, r2]
    assert m._roomsToReach == []


def test_corridor():
    m = Map(5)
    m.corridor(Coord(0, 1), Coord(4, 2))
    assert str(m) == "     \n.    \n.....\n     \n     \n"

    m.corridor(Coord(2, 0), Coord(3, 4))
    assert str(m) == "  .  \n. .  \n.....\n  .  \n  .. \n"


def test_move():
    h = Hero()
    m = Map(3, pos=Coord(0, 1), hero=h)
    m.put(Coord(0, 2), Element("Sword"))
    m.put(m._pos, h)
    assert str(m) == "   \n@  \nS  \n"
    assert m._hero.description() == "<Hero>(10)[]"
    m.move(m._hero, Coord(0, 1))
    assert str(m) == "   \n@  \n.  \n"
    assert m._hero.description() == "<Hero>(10)[S]"
    assert m._elem == {m._hero: Coord(0, 1)}


def test_map():
    h = Hero()
    m = Map(3, hero=h)
    m.put(m._pos, h)
    assert str(m) == "   \n @ \n   \n"
    assert m._hero.description() == "<Hero>(10)[]"
    assert m._elem[m._hero] == Coord(1, 1)
