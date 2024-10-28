from Element.Elements import Creature, Element
from Maping.Map import Coord, Map

m = Map(10)
m.put(Coord(6, 3), Creature("Goblin", 5, _strength=3))
m.put(Coord(0, 4), Creature("Snake", 5))
m.put(Coord(7, 7), Creature("Snake", 5))
m.put(Coord(6, 8), Element("gold", "o"))
m.put(Coord(4, 8), Element("gold", "o"))
m.play()
