import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Project.Element.Element import Element


def test_initialisation():
    o = Element("sword", "T")
    assert o._name == "sword"
    assert o._abbrv == "T"
    assert str(o) == "T"

    o = Element("gold")
    assert o._name == "gold"
    assert o._abbrv == "g"
    assert str(o) == "g"
