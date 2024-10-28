import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Project.Maping.Coord import Coord
from Project.Maping.Room import Room


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
