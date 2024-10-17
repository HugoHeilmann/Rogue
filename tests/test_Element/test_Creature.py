import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Creature import Creature
from Project.Element.Element import Element


def test_initialisation():
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