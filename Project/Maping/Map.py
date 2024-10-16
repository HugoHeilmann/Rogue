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
        self._mat[self.pos.x][self.pos.y] = hero

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
