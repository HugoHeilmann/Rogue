import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Elements import Element, Hero


def test_initialisation():
    h = Hero()
    assert h._name == "Hero"
    assert h._abbrv == "@"
    assert h._hp == 10
    assert h._strength == 2
    assert h._inventory == []


def test_take():
    h = Hero()
    s = Element("sword")
    h.take(s)
    assert h._inventory == [s]
    assert h.description() == "<Hero>(10)[s]"


def test_description():
    h = Hero()
    assert h.description() == "<Hero>(10)[]"
