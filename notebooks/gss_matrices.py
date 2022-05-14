"""
in dummy  s
out matrices      m
out test1          s
"""

from mathutils import Matrix

fn = '/home/elfnor/beasthoard/gits/eisenscript_to_xml/notebooks/ring_es2.gss'

with open(fn, 'r') as f:
    data = f.readlines()

mats= []
for d in data:
    m = d.strip().split(' ')
    m = [float(n) for n in m[1:17]]
    m = [m[n:n+4] for n in range(0, len(m), 4) ]
    mats.append(Matrix(m).transposed())

matrices = mats
test1 = [len(data)]