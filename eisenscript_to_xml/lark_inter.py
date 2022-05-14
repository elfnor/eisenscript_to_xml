"""
Translates the eisen script files used by StructureSynth
http://structuresynth.sourceforge.net/reference.php
into the eisenxml files used by the GenerativeArt node of the Sverchok addon for 
Blender


This translator ignores all commands to do with color or raytracing

Now uses lark parser

"""
from xml.etree import ElementTree as et
from xml.dom import minidom

from lark import Lark
from lark.visitors import Interpreter, v_args


parser = Lark.open("eisenscript.lark", rel_to=__file__)


def pre_process_es(es_text):
    """simple text substitution of #define"""
    es_lines = es_text.splitlines()
    format_dict = {}
    new_lines = []
    for line in es_lines:
        if line.startswith("#define"):
            parts = line.split()
            if len(parts) >= 3:
                format_dict[parts[1]] = " ".join(parts[2:])
        else:
            for key, item in format_dict.items():
                line = line.replace(key, item)
            new_lines.append(line)
    return "\n".join(new_lines)


def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = et.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class Iesxml(Interpreter):
    def convert(self, tree):
        self.xmltree = et.Element("rules")
        self.active = self.xmltree
        self._visit_tree(tree)
        self._scale_weights()
        return prettify(self.xmltree)

    def _scale_weights(self):
        # convert weights to integers
        rules = self.xmltree.findall("rule")
        weights = [float(rule.get("weight", 1)) for rule in rules[1:]]
        if min(weights) < 1:
            wscale = int(1 / min(weights))
            new_weights = [int(wscale * w) for w in weights]
            for w, rule in zip(new_weights, rules[1:]):
                rule.set("weight", f"{w}")

    def main(self, tree):
        self.visit_children(tree)

    def entry(self, tree):
        self.active = et.SubElement(self.xmltree, "rule")
        self.active.set("name", "entry")
        self.visit_children(tree)
        self.active = self.xmltree

    def ruledef(self, tree):
        # the xml creation happens in children
        self.active = et.SubElement(self.xmltree, "rule")
        self.visit_children(tree)
        self.active = self.xmltree

    def call(self, tree):
        """
        most of the logic and xml generation happens here
        data has structure
        multiple loops
        data = [{'count': '10', 'tgroup': 'tx 1', 'rname': 'r1_00'},
                {'count': '20', 'tgroup': 'ty 2', 'rname': 'r1_01'},
                {'count': '5', 'tgroup': 'tz 3', 'rname': 'r1'}]
        single loop
        data = [{'count': '1', 'tgroup': 'tx 1', 'rname': 'r1}]
        """
        data = self.visit_children(tree)
        rname = data[-1]
        data = data[:-1]
        # make the last loop rname and create names for any previous extra loops
        data[-1]["rname"] = rname
        for i, loop_dict in enumerate(data[:-1]):
            loop_dict["rname"] = f"{rname}_{i:02}"

        # the first loop is a call within the current rule
        if rname in ["box", "grid", "sphere", "line", "dot", "mesh"]:
            call = et.SubElement(self.active, "instance")
            call.set("shape", data[0]["rname"])
        else:
            call = et.SubElement(self.active, "call")
            call.set("rule", data[0]["rname"])

        call.set("count", data[0]["count"])
        call.set("transforms", data[0]["tgroup"])

        # subsequent loops are converted to rules with a single call to the next rule
        for i, loop_dict in enumerate(data[1:]):
            self.active = et.SubElement(self.xmltree, "rule")
            self.active.set("name", data[i]["rname"])
            call = et.SubElement(self.active, "call")
            call.set("rule", loop_dict["rname"])
            call.set("count", loop_dict["count"])
            call.set("transforms", loop_dict["tgroup"])

    def transgroup(self, tree):
        # joins all the transforms inside {} into a string
        data = " ".join(self.visit_children(tree))
        return data.strip()

    @v_args(meta=True)
    def trans(self, kids, meta):
        # called for each transform, returns a string
        tid = meta[0]
        values = meta[1:]

        if tid == "s" and len(values) == 1:
            tid = "sa"
        if tid in ("x", "y", "z"):
            tid = "t" + tid
        if tid in ("tx", "ty", "tz", "rx", "ry", "rz", "sa", "s"):
            tstr = tid + " " + " ".join(values)
        else:
            tstr = ""
        return tstr.strip()

    def loop(self, tree):
        # an optional count and the list of transforms in {} brackets
        # creates a dict containing count and transform group
        data = self.visit_children(tree)
        # print(data)
        if len(data) == 0:
            loop_dict = {"count": "1", "tgroup": ""}
        if len(data) == 1:
            loop_dict = {"count": "1", "tgroup": data[0]}
        if len(data) == 2:
            loop_dict = {"count": data[0], "tgroup": data[1]}

        return loop_dict

    @v_args(inline=True)
    def rulename(self, rname):
        rname = rname.split(":")[0]
        return str(rname)

    @v_args(inline=True)
    def repeat(self, c):
        return str(c)

    @v_args(inline=True)
    def rulenamedef(self, rname):
        self.active.set("name", rname)

    @v_args(inline=True)
    def wmod(self, weight):
        self.active.set("weight", weight)

    @v_args(meta=True)
    def mmod(self, kids, meta):
        self.active.set("max_depth", meta[0])
        if len(meta) > 1:
            self.active.set("successor", meta[1])

    def setblock(self, tree):
        self.visit_children(tree)

    @v_args(meta=True)
    def setatr(self, kids, meta):
        atr = meta[0]
        values = meta[1:]
        if atr == "maxdepth":
            self.xmltree.set("max_depth", str(values[0]))

    @v_args(inline=True)
    def define(self, varname, value):
        const = et.SubElement(self.xmltree, "constants")
        const.set(varname, value)
