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
    assert map._elem["@"] == Coord(1, 1)


def test_len():
    map = Map()
    assert len(map) == 5
    map = Map(3)
    assert len(map) == 3


def test_str():
    map = Map(3, Coord(0, 1))
    assert str(map) == ".@.\n...\n...\n"
