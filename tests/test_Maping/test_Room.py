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
