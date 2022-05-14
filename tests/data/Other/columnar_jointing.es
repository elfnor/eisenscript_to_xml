// https://github.com/kutsilyo/Structure_Synth_Creations/blob/main/Columnar%20Jointing/columnar%20jointing.es
set background #fff
set maxdepth 400

// based on the natural columnar jointing phenomenon 

5 * { x 10 hue -15 } column2

rule column2 {
	10 * { rx 360/10 z 2 } twist
}

rule twist {
	5 * { rx 360/10 x 2 y 1 hue -9 } colum
}

rule colum { 
	{ s 5 2 2 } box
}

rule base {
	{ x -1 y 5 z 5 s 2 5 6 } box
}

rule base {
	{ x -1 y -5 z -5 s 2 5 6 } box
}


