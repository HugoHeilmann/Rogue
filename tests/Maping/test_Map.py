from Project.Maping.Coord import Coord
from Project.Maping.Map import Map


def test_initialisation():
    map = Map()
    assert map.ground == "."
    assert map.dir["z"] == Coord(-1, 0)
    assert map.dir["q"] == Coord(0, -1)
    assert map.dir["s"] == Coord(1, 0)
    assert map.dir["d"] == Coord(0, 1)
