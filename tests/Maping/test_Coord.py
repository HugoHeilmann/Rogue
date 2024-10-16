from Project.Maping.Coord import Coord

def test_initialisation():
    coord = Coord(3, 0)
    assert coord.x == 3
    assert coord.y == 0