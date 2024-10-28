import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Elements import Hero
from Project.Game.Game import Game


def test_initialisation():
    assert str(Game()._hero) == "@"
    assert Game()._level == 1
    assert Game()._floor == None
    assert Game()._message == []
    assert Game(level=3)._level == 3
    assert str(Game(hero=Hero("Conan"))._hero) == "@"
