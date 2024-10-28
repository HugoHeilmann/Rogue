import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Elements import Hero
from Project.Maping.Coord import Coord
from Project.Maping.Map import Map


def test_initialisation():
    map = Map()
    assert map.ground == "."
    assert map.dir["z"] == Coord(0, -1)
    assert map.dir["q"] == Coord(-1, 0)
    assert map.dir["s"] == Coord(0, 1)
    assert map.dir["d"] == Coord(1, 0)
    assert len(map._mat) == 5
    for i in range(len(map._mat)):
        assert len(map._mat[i]) == 5
    assert map._elem[str(map._hero)] == Coord(1, 1)


def test_len():
    map = Map()
    assert len(map) == 5
    map = Map(3)
    assert len(map) == 3


def test_contains():
    assert (Coord(0, 4) in Map()) == True
    assert (Coord(0, 4) in Map(3)) == False
    assert (Coord(0, 5) in Map()) == False
    assert (Coord(-1, 3) in Map()) == False
    assert (Coord(1, -1) in Map()) == False
    assert (Coord(5, 2) in Map()) == False
    assert (Coord(4, 4) in Map()) == True

    assert ("@" in Map()) == True
    assert ("X" in Map()) == False
    assert ("X" in Map(pos=Coord(4, 4), hero=Hero(_abbrv="X"))) == True


def test_str():
    map = Map(3, pos=Coord(0, 1))
    assert str(map) == "...\n@..\n...\n"


def test_get():
    assert Map().get(Coord(0, 4)) == "."
    assert Map().get(Coord(1, 1)) == "@"
    assert Map().get(Coord(2, 3)) == "."


def test_pos():
    map = Map(pos=Coord(1, 1), hero=Hero(_abbrv="@"))
    coord = map.get_pos("@")
    assert coord.x == 1
    assert coord.y == 1
    assert Map(pos=Coord(2, 3), hero=Hero(_abbrv="X")).get_pos("X") == Coord(2, 3)


def test_put():
    m = Map()
    m.put(Coord(3, 2), "X")
    m.put(Coord(0, 0), "A")
    assert str(m) == "A....\n.@...\n...X.\n.....\n.....\n"
    assert m._elem == {"@": Coord(1, 1), "X": Coord(3, 2), "A": Coord(0, 0)}


def test_way():
    m = Map(3)
    m.move("@", Coord(-1, 0))
    assert str(m) == "...\n@..\n...\n"
    assert m._elem == {"@": Coord(0, 1)}
    m.move("@", Coord(0, 1))
    assert str(m) == "...\n...\n@..\n"
    assert m._elem == {"@": Coord(0, 2)}


def test_map():
    m = Map(3)
    assert str(m) == "...\n.@.\n...\n"
    assert m._hero.description() == "<Hero>(10)[]"
    assert m._elem[str(m._hero)] == Coord(1, 1)
