import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Elements import *


# Element
def test_initialisation_element():
    o = Equipment("sword", "T")
    assert o._name == "sword"
    assert o._abbrv == "T"
    assert str(o) == "T"

    o = Equipment("gold")
    assert o._name == "gold"
    assert o._abbrv == "g"
    assert str(o) == "g"


def test_description():
    assert Element("sword").description() == "<sword>"
    assert Element("Gold").description() == "<Gold>"


def test_meet():
    hero = Hero()
    o = Element("Gold")
    assert o.meet(hero) == True
    assert hero.description() == "<Hero>(10)[G]"
    assert (o in hero._inventory) == True


# Equipment
def test_heritage():
    assert isinstance(Equipment("Sword"), Element) == True
    assert isinstance(Creature("Goblin", 5), Element) == True
    assert isinstance(Hero(), Element) == True
    assert isinstance(Creature("Goblin", 5), Equipment) == False
    assert isinstance(Element("XXX"), Equipment) == False


def test_meet():
    h = Hero()
    assert h.description() == "<Hero>(10)[]"
    o = Equipment("Golf")
    o.meet(h)
    assert h.description() == "<Hero>(10)[G]"
    assert (o in h._inventory) == True


# Creature
def test_initialisation_creature():
    o = Creature("Goblin", 10)
    assert o._name == "Goblin"
    assert o._abbrv == "G"
    assert o._hp == 10
    assert o._strength == 1

    em = Creature("Evil Mushroom", 15, "M", 3)
    assert em._name == "Evil Mushroom"
    assert em._abbrv == "M"
    assert em._hp == 15
    assert em._strength == 3


def test_heritage():
    assert isinstance(Creature("Goblin", 5), Element) == True


def test_description():
    assert Creature("Goblin", 9).description() == "<Goblin>(9)"
    assert Creature("Snake", 2).description() == "<Snake>(2)"


def test_meet():
    h = Hero()
    o = Creature("Ork", 3)
    assert o.meet(h) == False
    assert h.description() == "<Hero>(10)[]"
    assert o.description() == "<Ork>(1)"
    assert o.meet(h) == True
    assert h.description() == "<Hero>(10)[]"
    assert o.description() == "<Ork>(-1)"

    h = Hero(_hp=3, _strength=10)
    o = Creature(_name="Ork", _strength=10, _hp=12)
    assert o.meet(h) == False
    assert h.description() == "<Hero>(3)[]"
    assert o.description() == "<Ork>(2)"


# Hero
def test_initialisation_hero():
    h = Hero()
    assert h._name == "Hero"
    assert h._abbrv == "@"
    assert h._hp == 10
    assert h._strength == 2
    assert h._inventory == []


def test_take():
    h = Hero()
    s = Equipment("sword")
    h.take(s)
    assert h._inventory == [s]
    assert h.description() == "<Hero>(10)[s]"


def test_description():
    h = Hero()
    assert h.description() == "<Hero>(10)[]"
