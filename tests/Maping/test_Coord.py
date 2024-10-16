from Project.Maping.Coord import Coord


def test_initialisation():
    coord = Coord(3, 0)
    assert coord.x == 3
    assert coord.y == 0


def test_equals():
    c1 = Coord(3, 4)
    c2 = Coord(3, 4)
    c3 = Coord(4, 4)
    assert (c1 == c2) == True
    assert (c2 == c1) == True
    assert (c1 == c3) == False


def test_str():
    c1 = Coord(3, 4)
    c2 = Coord(0, 0)
    assert str(c1) == "<3,4>"
    assert str(c2) == "<0,0>"
