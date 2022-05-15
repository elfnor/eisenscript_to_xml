# Eisenscript to XML

Eisenscript is a domain specific language (DSL) designed by Mikael Hvidtfeldt for generating 3d structures. 

The original use was in [Structure Synth](http://structuresynth.sourceforge.net). 

The original reference for the langauge is here:
http://structuresynth.sourceforge.net/reference.php


The [Sverchok](http://nortikin.github.io/sverchok/) add-on for [Blender](https://www.blender.org/) has a node [Generative Art](http://nortikin.github.io/sverchok/docs/nodes/script/generative_art.html) that can produce similar structures. It uses an xml version of the eisenscript DSL (eisenxml) based on  prideout's [lsystem](https://github.com/prideout/lsystem) code.

This package translates from the original eisenscript to the eisenxml used by the Sverchok Generative Art node.

An earlier version is avaliable in [
eisenscript_to_xml.py](https://github.com/elfnor/generative-art-examples) but this does not work with later versions of pyparsing (last seen working with pyparsing 2.1.3.).  This version uses the [lark parser](https://lark-parser.readthedocs.io/en/latest/) to define a grammar to parse and translate the eisenscript.

A version of the matrix generator used in the Sverchok node is included in `generative_art.py` for testing purposes. 


A collection of working examples from Structure Synth is avaliable in the examples folder, along with eisenxml translations and screenshots from both Structure Synth and Blender.

This is in a mostly works state for small examples, and should help someone transtion from Structure Synth to Sverchok Generative Art. It does not attempt to translate any of the colour commands avaialble in Structure Synth as they're not implemented in the SV node. 

Its very easy to write valid Structure Synth eisenscript that's breaks this, and I don't intend it to cover every possiblilty. Treat it more as learning and transitioning tool to work with small examples. 

## Usage

```
from eisenscript_to_xml.lark_inter import translate

es_str = """ 
36 * { rz 10  y 1   }   36 * { ry 10  z 1.2  } xbox
rule xbox { box}
"""
xml_str = translate(es_str)
print(xml_str)
```

```
<?xml version="1.0" ?>
<rules max_depth="100">
  <rule name="entry">
    <call rule="xbox_00" count="36" transforms="rz 10 ty 1"/>
  </rule>
  <rule name="xbox_00">
    <call rule="xbox" count="36" transforms="ry 10 tz 1.2"/>
  </rule>
  <rule name="xbox">
    <instance shape="box"/>
  </rule>
</rules>
```

## Eisenscipt elsewhere

Original
http://structuresynth.sourceforge.net/index.php

Python - C++ - Go - original base for Sverchok Generative Art node
https://github.com/prideout/lsystem

Rust implentation
https://github.com/TannerRogalsky/eisenscript

BrowserSynth - Javascript
https://github.com/kronpano/BrowserSynth

Online
https://kronpano.github.io/BrowserSynth/

Javascript
https://github.com/after12am/eisenscript

Online
https://after12am.github.io/eisenscript-editor/?show=0

