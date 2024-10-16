from Project.Maping.Coord import Coord


class Map:
    ground = "."
    dir = {"z": Coord(-1, 0), "q": Coord(0, -1), "s": Coord(1, 0), "d": Coord(0, 1)}
