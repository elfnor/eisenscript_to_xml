# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

""" by Eleanor Howick | 2015 https://github.com/elfnor
    LSystem code from Philip Rideout  https://github.com/prideout/lsystem """

""" this is a copy from 
   https://github.com/nortikin/sverchok/blob/165a9bf4c217823a205500319e7586f07ca1886a/nodes/script/generative_art.py
   with sverchok/blender stuff striped, and mathutils replaced with euclid
   "https://github.com/r1chardj0n3s/euclid"
   and takes an xml_text string  as input , includes the preformat constant substitution

"""
import random
from xml.etree import ElementTree as et
from euclid import Matrix4

"""
---------------------------------------------------
    LSystem
---------------------------------------------------
"""


class LSystem:

    """
    This copy takes an xml_text str as input
    """

    def __init__(self, xml, maxObjects):

        self.xml_text = xml
        self._tree = et.fromstring(self.xml_text)

        self._maxDepth = int(self._tree.get("max_depth"))
        self._progressCount = 0
        self._maxObjects = maxObjects
        self._xml_text_preformat()

    def _xml_text_preformat(self):
        """
        substitute constants from xml
        """
        # get constants from xml
        format_dict = {}

        for elem in self._tree.findall("constants"):
            format_dict.update(elem.attrib)

        self.xml_text = str(self.xml_text)

        while "{" in str(self.xml_text):
            # using while loop
            # allows constants to be defined using other constants
            self.xml_text = self.xml_text.format(**format_dict)

        self._tree = et.fromstring(self.xml_text)

    def evaluate(self, seed=0):
        """
        Returns a list of "shapes".
        Each shape is a 2-tuple: (shape name, transform matrix).
        """
        random.seed(seed)
        rule = _pickRule(self._tree, "entry")
        entry = (rule, 0, Matrix4.new_identity())
        shapes = self._evaluate(entry)
        return shapes

    def _evaluate(self, entry):
        stack = [entry]
        shapes = []
        nobjects = 0
        while len(stack) > 0:
            if nobjects > self._maxObjects:
                print("max objects reached")
                break

            rule, depth, matrix = stack.pop()

            local_max_depth = self._maxDepth
            if "max_depth" in rule.attrib:
                local_max_depth = int(rule.get("max_depth"))

            if len(stack) > self._maxDepth:
                shapes.append(None)
                continue

            if depth > local_max_depth:
                if "successor" in rule.attrib:
                    successor = rule.get("successor")
                    rule = _pickRule(self._tree, successor)
                    stack.append((rule, 0, matrix))
                shapes.append(None)
                continue

            base_matrix = matrix.copy()
            for statement in rule:
                tstr = statement.get("transforms", "")
                if not (tstr):
                    tstr = ""
                    for t in [
                        "tx",
                        "ty",
                        "tz",
                        "rx",
                        "ry",
                        "rz",
                        "sa",
                        "sx",
                        "sy",
                        "sz",
                    ]:
                        tvalue = statement.get(t)
                        if tvalue:
                            n = eval(tvalue)
                            tstr += "{} {:f} ".format(t, n)
                xform = _parseXform(tstr)
                count = int(statement.get("count", 1))
                count_xform = Matrix4.new_identity()
                for n in range(count):
                    count_xform *= xform
                    matrix = base_matrix * count_xform

                    if statement.tag == "call":
                        rule = _pickRule(self._tree, statement.get("rule"))
                        cloned_matrix = matrix.copy()
                        entry = (rule, depth + 1, cloned_matrix)
                        stack.append(entry)

                    elif statement.tag == "instance":
                        name = statement.get("shape")
                        if name == "None":
                            shapes.append(None)
                        else:
                            shape = (name, matrix)
                            shapes.append(shape)
                            nobjects += 1

                    else:
                        raise ValueError("bad xml", statement.tag)

                if count > 1:
                    shapes.append(None)

        return shapes
        # end of _evaluate


def _pickRule(tree, name):

    rules = tree.findall("rule")
    elements = []
    for r in rules:
        if r.get("name") == name:
            elements.append(r)

    if len(elements) == 0:
        raise ValueError("bad xml", "no rules found with name '%s'" % name)

    sum, tuples = 0, []
    for e in elements:
        weight = int(e.get("weight", 1))
        sum = sum + weight
        tuples.append((e, weight))
    n = random.randint(0, sum - 1)
    for (item, weight) in tuples:
        if n < weight:
            break
        n = n - weight
    return item


_xformCache = {}


def _parseXform(xform_string):
    if xform_string in _xformCache:
        return _xformCache[xform_string]

    matrix = Matrix4.new_identity()
    tokens = xform_string.split()
    t = 0
    while t < len(tokens) - 1:
        command, t = tokens[t], t + 1

        # Translation
        if command == "tx":
            x, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_translate(x, 0, 0)

        elif command == "ty":
            y, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_translate(0, y, 0)
        elif command == "tz":
            z, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_translate(0, 0, z)
        elif command == "t":
            x, t = eval(tokens[t]), t + 1
            y, t = eval(tokens[t]), t + 1
            z, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_translate(x, y, z)

        # Rotation
        elif command == "rx":
            theta, t = _radians(eval(tokens[t])), t + 1
            matrix *= Matrix4.new_rotatex(theta)

        elif command == "ry":
            theta, t = _radians(eval(tokens[t])), t + 1
            matrix *= Matrix4.new_rotatey(theta)
        elif command == "rz":
            theta, t = _radians(eval(tokens[t])), t + 1
            matrix *= Matrix4.new_rotatez(theta)

        # Scale
        elif command == "sx":
            x, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_scale(x, 1, 1)
        elif command == "sy":
            y, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_scale(1, y, 1)
        elif command == "sz":
            z, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_scale(1, 1, z)
        elif command == "sa":
            v, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_scale(v, v, v)
        elif command == "s":
            x, t = eval(tokens[t]), t + 1
            y, t = eval(tokens[t]), t + 1
            z, t = eval(tokens[t]), t + 1
            matrix *= Matrix4.new_scale(x, y, z)

        else:
            err_str = "unrecognized transform: '%s' at position %d in '%s'" % (
                command,
                t,
                xform_string,
            )
            raise ValueError("bad xml", err_str)

    _xformCache[xform_string] = matrix
    return matrix


def _radians(d):
    return float(d * 3.141 / 180.0)
