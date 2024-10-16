from Project.Maping.Coord import Coord


class Map:
    ground = "."
    dir = {"z": Coord(0, -1), "q": Coord(-1, 0), "s": Coord(0, 1), "d": Coord(1, 0)}

    def __init__(
        self, size: int = 5, pos: Coord = Coord(1, 1), hero: str = "@"
    ) -> None:
        self.size = size
        self.pos = pos
        self.hero = hero
        self._mat = [[Map.ground for _ in range(size)] for _ in range(size)]
        self._elem = {hero: pos}
        self.put(pos, hero)

    def __len__(self) -> int:
        return len(self._mat)

    def __contains__(self, item) -> bool:
        if isinstance(item, Coord):
            return (
                item.x >= 0
                and item.x < len(self)
                and item.y >= 0
                and item.y < len(self)
            )
        else:
            return item in self._elem

    def __repr__(self) -> str:
        matrix = ""
        for i in range(len(self._mat)):
            for j in self._mat[i]:
                matrix += j
            matrix += "\n"
        return matrix

    def get(self, c: Coord) -> str:
        return self._mat[c.y][c.x]

    def pos(self, e) -> Coord:
        return self._elem[e]

    def put(self, c: Coord, e) -> None:
        self._mat[c.y][c.x] = e
        self._elem[e] = c

    def rm(self, c: Coord) -> None:
        self._mat[c.y][c.x] = self.ground
        del self._elem[self.get(c)]
