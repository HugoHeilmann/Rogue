class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: "Coord") -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"<{self.x},{self.y}>"
