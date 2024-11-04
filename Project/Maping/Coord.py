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

    def direction(self, other: "Coord") -> "Coord":
        diff: Coord = other - self
        dist = self.distance(other)

        if dist == 0:
            return Coord(0, 0)

        norm_x = diff.x / dist
        norm_y = diff.y / dist

        direction_x = 0
        direction_y = 0

        if norm_x > 0:
            direction_x = 1
        elif norm_x < 0:
            direction_x = -1

        if norm_y > 0:
            direction_y = 1
        elif norm_y < 0:
            direction_y = -1

        return Coord(direction_x, direction_y)
