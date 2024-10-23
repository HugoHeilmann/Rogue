import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Elements import Element, Hero


def test_initialisation():
    o = Element("sword", "T")
    assert o._name == "sword"
    assert o._abbrv == "T"
    assert str(o) == "T"

    o = Element("gold")
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
