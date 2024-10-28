from .Coord import Coord


class Room:
    def __init__(self, c1: Coord, c2: Coord) -> None:
        self._c1 = c1
        self._c2 = c2

    def __repr__(self) -> str:
        return f"[<{self._c1.x},{self._c1.y}>,<{self._c2.x},{self._c2.y}>]"

    def __contains__(self, c: Coord) -> bool:
        return (
            c.x >= self._c1.x
            and c.x <= self._c2.x
            and c.y >= self._c1.y
            and c.y <= self._c2.y
        )

    def center(self) -> Coord:
        res: Coord = Coord(0, 0)
        res.x = (self._c1.x + self._c2.x) // 2
        res.y = (self._c1.y + self._c2.y) // 2
        return res

    def intersect(self, r: "Room") -> bool:
        c3 = Coord(self._c2.x, self._c1.y)
        c4 = Coord(self._c1.x, self._c2.y)
        return self._c1 in r or self._c2 in r or c3 in r or c4 in r
