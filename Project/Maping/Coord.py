import math


class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: "Coord") -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coord") -> "Coord":
        return Coord(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"<{self.x},{self.y}>"

    def distance(self, other: "Coord") -> int:
        sqrx: int = math.pow((other.x - self.x), 2)
        sqry: int = math.pow((other.y - self.y), 2)
        return math.sqrt(sqrx + sqry)
