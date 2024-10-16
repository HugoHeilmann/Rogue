from Project.Maping.Coord import Coord


class Map:
    ground = "."
    dir = {"z": Coord(-1, 0), "q": Coord(0, -1), "s": Coord(1, 0), "d": Coord(0, 1)}

    def __init__(
        self, size: int = 5, pos: Coord = Coord(1, 1), hero: str = "@"
    ) -> None:
        self.size = size
        self.pos = pos
        self.hero = hero
        self._mat = [[Map.ground for _ in range(size)] for _ in range(size)]
        self._elem = {hero: pos}
