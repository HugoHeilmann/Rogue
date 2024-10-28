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
