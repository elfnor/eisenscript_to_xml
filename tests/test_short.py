"""
things to cover in tests (- done * todo)
working through Examples adding fails here 

- call/shape with no loop
- call with loop
- loop containing only color transforms
- call with loop and count
- call with multiple loops
- shape instance
- rule with multiple calls
- floats, integers and signed versions 
* floats for weight - Sverchok xml parser expects int
- s with 1 value, s with 3 values transform

- rule with max depth
- rule with max depth and successor rule
- combinations of weight and max depth
- multiple weighted defintiions of the same rule
- "rule" keyword can also be "Rule"

- set blocks
- colons in atribute names "set raytracer::shadows false"
- dash in attribute names "set raytracer::max-depth 5"
- commas in triples in set statements
- color transforms are ignored
- cpp comments
- c comments
- # define 
- constants in maxdepth
- constants that start with one of VID sequences

- expressions in floats ie "360/10" , SS seems to parse "/" but not much else
"""


import pytest

from eisenscript_to_xml.lark_inter import Iesxml, parser, pre_process_es
from eisenscript_to_xml.generative_art import LSystem

"""
all of the below should produce 10 objects
spaced around a ring in the xy plane, radius 10, centered on origin
but each tests different parts of the grammar parser
"""

# single call with loop and count
# call with loop no count
# signed floats
# s with 1 value
ring_a = """set maxdepth 20
10 * { rz -36.0 }  dbox
rule dbox {
 {x +10.0 s 1}  box
}
"""

# multiple loops on one call
# shape call with no loop
# multiple transforms in loop
# unsigned float
# unsigned integer
# loop with only color transforms
# capitalise "Rule"
ring_b = """set maxdepth 20
10 * {rz 36 } 1 * { x 10.0 rz 180}  dbox

Rule dbox {
  {hue 0.5 brightness 0.9 alpha 0.4} box
}
"""

# rule call with no loop
# rule definition with loop and count
# signed integers
# cpp comments
# s with 3 values
ring_c = """set maxdepth 20
// here is the entry rule
r1

// and here are the rule definitions
rule r1 {
  10 * { rz -36 }  dbox
}
rule dbox {
 {x +10 s 1 1 1 }  box
}
"""

# multiple weighted defintions of the same rule
# weights less than 1
ring_d = """set maxdepth 20
10 * { rz 36 }  dbox

rule dbox w 1{
 {x 9.999} box
}

rule dbox w 0.5{
{ x 10.001  } box
}"""

# max depth
# shape call in entry calls
# rule with multiple calls
# ignore "set seed initial"
ring_e = """set maxdepth 20
dbox
{rz -36 x 10 } box

rule dbox md 9{
  set seed initial
  { rz 36} dbox
  {x 10} box
}"""

# max depth with successor rule
# color names
# color hex
# strength argument on blend
ring_f = """set maxdepth 20
dbox

rule dbox md 9 > lastbox{
  { rz 36} dbox
  {x 10 color my_shade_of_red blend red } box
}

rule lastbox {
{ x  10 color #8B0001 blend red 0.02} box
}"""

# weight and md combinations
# set blocks
# commas in triples
# cpp comments
# c comment block
# box::shiny - FAILS
ring_g = """
/* 
   c comment block
   to ignore 
*/

// ------ Camera settings.
set translation [0 -0.367113 -20]
set rotation [0.963994 0.0575931 -0.259613 0.0514549 0.917418 0.394584 0.260899 -0.393735 0.881422]
set pivot [0 0 0]
set scale 0.408795
set maxdepth 20
set raytracer::shadows false
set raytracer::phong [0.5,0.4,0.2]
set raytracer::max-depth 5

dbox

rule dbox weight 10 md 9 > lastbox{
  { rz 36} dbox
  {x 10 } box
}

rule dbox w 1 maxdepth 10 {
  { rz 36} dbox
  {x 10 } box
}

rule lastbox {
{ x  10 } box::shiny
}"""

# #define preprocessor
# at front
# later on
# constant includes undescore
ring_h = """#define angle 36
set maxdepth 20
10 * { rz angle}  dbox
#define _radius 10
rule dbox {
 {x _radius }  box
}
"""

# #define between rules
# constant includes transform id
ring_i = """set maxdepth 20
#define angle 36
10 * { rz angle}  dbox

rule dbox w 10{
 {x 9.999} box
}
#define shrink s 0.996
rule dbox w 5{
{ shrink x 10.001  } box
}"""

# constant with negative sign
# division in float
ring_j = """set maxdepth 20

#define _f1 1.0
#define _f2 1.0
#define _f3 1.0

10 * { rz 360/10}  dbox

rule dbox w 5{
{ s _f1 _f2 -_f3 x 10  } box
}"""


@pytest.mark.parametrize(
    "es_str",
    [ring_a, ring_b, ring_c, ring_d, ring_e, ring_f, ring_g, ring_h, ring_i, ring_j],
    ids=[
        "ring_a",
        "ring_b",
        "ring_c",
        "ring_d",
        "ring_e",
        "ring_f",
        "ring_g",
        "ring_h",
        "ring_i",
        "ring_j",
    ],
)
def test_convert(es_str):
    es_str = pre_process_es(es_str)
    test = parser.parse(es_str)
    xml_str = Iesxml().convert(test)
    lsys = LSystem(xml_str, 100)
    shapes = lsys.evaluate(0)
    # count shapes that are not None
    assert len([s for s in shapes if s]) == 10
