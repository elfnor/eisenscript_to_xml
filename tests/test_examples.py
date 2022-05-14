"""
trys to convert es files in tests/data/Examples to eisenxml

GOOD
see working list below

BAD

Examples/Arc Sphere.es - endless loop in Lsystem?
does something odd with the sub-rules

"Moduli Creatures.es" and "Thingy.es" fail randomly? 


NOT TO FIX - makes no sense as not-implemented in GA Sverchok 
Examples/Tutorials/TriangleComposites.es - "triangle[0,0,0;1,0,0;0.5,0.5,0.5]"
Examples/Tutorials/PreprocessorGUI.es - "#define sizeStep 0.94 (float:0-1)"
Examples/Tutorials/CSG test.es - "template::intersection-begin"
Examples/Tutorials/JavaScript - Movie.es - "#javascript"
Examples/Tutorials/NouveauMovie.es - n=more movie javscript stuff
Examples/MeshTest.es - "mesh"

"""

import pytest


from eisenscript_to_xml.lark_inter import Iesxml, parser, pre_process_es
from eisenscript_to_xml.generative_art import LSystem
from eisenscript_to_xml import EXAMPLES_ES

working = [
    "Ball.es",
    "BinaryKite.es",
    "City of Glass.es",
    "Default.es",
    "Frame In Frame.es",
    "Grinder.es",
    "Konstrukt.es",
    "Menger.es",
    "Moduli Creatures.es",
    "Mondrian.es",
    "Nabla.es",
    "NineWorthies.es",
    "Nouveau.es",
    "Nouveau2.es",
    "Nouveau3.es",
    "Octopod II.es",
    "Reflection.es",
    "RoundTree.es",
    "SpiralTree2D.es",
    "Synctor.es",
    "Thingy.es",
    "Torus2.es",
    "Torus3.es",
]


@pytest.mark.parametrize("fn", working)
def test_convert(fn):

    with (EXAMPLES_ES / fn).open() as f:
        es_str = f.read()
    es_str = pre_process_es(es_str)
    test = parser.parse(es_str)
    xml_str = Iesxml().convert(test)
    lsys = LSystem(xml_str, 100)
    shapes = lsys.evaluate(0)
    # count shapes that are not None
    # will eventually get expected values for count from Structure Synth
    assert len([s for s in shapes if s]) > 0
