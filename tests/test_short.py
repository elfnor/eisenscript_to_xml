# just droppping intereting examples for now
# they test grammar  and may not be interesting geometrically.

# multiple loops per call

oct2 = """set maxdepth 100

10 * { x 1} 20 * { y 2 } 30 * { z 3  } r1

rule r1  {
    box
}"""

# successor rule

ball = """set maxdepth 2000
R1 

rule R1 w 10 md 20 > R2  { 
{ x 1  } R1
{ s 1 1 0.1 } box
} 
rule R2  { 
sphere
} 
"""

# minimal example with loop repeat

test = """ 2 * { x 1 y 2} seed
{ rx 1 ry 2} seed
rule seed  { 
  box 
}
"""

# things to cover in tests

# call with no loop
# call with loop
# call with loop and count
# call with multiple loops
# shape instance
# rule call

# rule with weight
# rule with max depth
# rule with max depth and successor rule
# combinations of weight and max depth

# multiple defintiions of the same rule

# set directives

# color transforms are ignored
