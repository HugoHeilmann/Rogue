import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import random

from Project.Element.Elements import Equipment, Hero
from Project.Game.Game import Game
from Project.Maping.Map import Map


def test_initialisation():
    assert str(Game()._hero) == "@"
    assert Game()._level == 1
    assert Game()._floor == None
    assert Game()._message == []
    assert Game(level=3)._level == 3
    assert str(Game(hero=Hero("Conan"))._hero) == "@"

    assert str(Game.equipments) == "{0: [!, o], 1: [s, b], 2: [c]}"
    assert str(Game.monsters) == "{0: [G, W], 1: [O, B], 5: [D]}"


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


def test_rand():
    assert str(Game().randElement({0: [Equipment("x")]})) == "x"

    random.seed(42)
    g = Game()
    assert g.randEquipment().description() == "<sword>"
    assert g.randEquipment().description() == "<sword>"
    assert g.randEquipment().description() == "<potion>"
    assert g.randMonster().description() == "<Ork>(6)"
    assert g.randMonster().description() == "<Goblin>(4)"
    assert g.randMonster().description() == "<Goblin>(4)"
