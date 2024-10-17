from .Coord import Coord


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
        self._elem = {}
        self.put(pos, hero)

    def __len__(self) -> int:
        return len(self._mat)

    def __contains__(self, item) -> bool:
        if isinstance(item, Coord):
            return 0 <= item.x < len(self) and 0 <= item.y < len(self)
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

    def get_pos(self, e) -> Coord:
        return self._elem[e]

    def put(self, c: Coord, e) -> None:
        self._mat[c.y][c.x] = e
        self._elem[e] = c

    def rm(self, c: Coord) -> None:
        elem = self.get(c)
        if elem in self._elem:
            self._mat[c.y][c.x] = self.ground
            del self._elem[elem]

    def move(self, e, way: Coord) -> None:
        if self.get_pos(e) + way in self:
            last_pos = self.get_pos(e)
            self.rm(last_pos)
            self.put((last_pos + way), e)

    def play(self, hero="@"):
        while True:
            print(self)
            self.move(hero, Map.dir[getch()])


def getch():
    try:
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        import msvcrt

        return msvcrt.getch().decode("utf-8")
