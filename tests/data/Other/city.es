// https://github.com/kutsilyo/Structure_Synth_Creations/blob/main/City/city.es
set background #fffcf1
set maxobjects 120000
set colorpool list:#a06389,#e1aea4,#ffecb2,#684971,#cb7ca2,#f9d8a1

// generates a city
// tries to create the effect of a skyline where the buildings at
// the edges are smaller

city

rule city {
	4 * { ry 90 x -25 z 14 } cityquad
}

rule cityquad {
	4 * { x 15  z 1 s 0.88 color random} cityrow2
}

rule cityrow2 {
	{ color random} cityblock
	3 * { z 15 s 0.88 color random} cityblock // x 1 
}

rule cityblock {
	2 * { x 6 s 0.9} cityrow1
}

rule cityrow1 {
	2 * { z 6 color random s 0.9} building
}

rule building {
	15 * { y 1 ry 90 x -6 } floor
}

rule building w 1.1 {
	10 * { y 1 ry 90 x -6 } floor
}

rule floor {
	5 * { x 1 } row
}

rule floor {
	4 * { x 1 } row
 }

rule building {
	5 * { y 1 ry 90 x -6 } floor
}

rule row {
	5 * { z 1 } room
}

rule row {
	4 * { z 1 } room
}

rule room {
	{ } box //color #a06389
}

rule room {
	{ } grid //color #000
}

rule room {
	{ } xbox //color #000
}

rule xbox w 1.1 {
	{ s 0.9 } box //color #fff 
	{ color random } grid //color #fffcf1
}

rule lbox {
	{ s 2 1 1 } box
}