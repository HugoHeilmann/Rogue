import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import random

from Project.Element.Elements import Hero
from Project.Game.Game import Game
from Project.Maping.Map import Map


def test_initialisation():
    assert str(Game()._hero) == "@"
    assert Game()._level == 1
    assert Game()._floor == None
    assert Game()._message == []
    assert Game(level=3)._level == 3
    assert str(Game(hero=Hero("Conan"))._hero) == "@"


def test_buildFloor():
    random.seed(42)
    g = Game()
    assert g._floor == None
    g.buildFloor()
    assert g._floor != None
    assert isinstance(g._floor, Map) == True


def test_messages():
    g = Game()
    assert g.readMessages() == ""
    g.addMessage("Bonjour")
    g.addMessage("Let's play")
    assert g.readMessages() == "Bonjour. Let's play. "
    assert g.readMessages() == ""
