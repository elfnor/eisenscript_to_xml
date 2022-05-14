
// Structure Synth Pov Ray Export. 

// Global settings
global_settings {
  max_trace_level 5
  ambient_light rgb <1,1,1>
}

#default {
  texture { 
    pigment { color rgb 1 }
    finish { ambient 0.1 diffuse 0.5 specular 0.5 }
   normal { dents 0 scale 0.01 }
  }
}
    
// Background
plane {
  z, 100.0
  texture {
	pigment { color rgb <0.0,0.0,0.0> }
	finish { ambient 1 }
  }
  hollow
}

// Camera
camera {
  location <-1.04724,2.10168,59.9545>
  right <-0.99558*1.61642,-0.0928962*1.61642,-0.0138158*1.61642>
  up <-0.0923411,0.995059,-0.0364924>
  look_at <2.72308,-5.61097,-159.88>

}

// Lights
light_source { <500,500,-1000> rgb <1,1,1>  } 
light_source { <-500,-500,-1000> rgb <1,1,1>  } 
light_source { <-500,500,1000> rgb <1,1,1>  } 
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < -0.809017, -0.587785, 0, 0.587786, -0.809017, 0, 0, 0, 1, 8.70079, 7.07625, 0 > 
  texture { pigment { color rgbt <1,0.0166667,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < -0.309017, -0.951056, 0, 0.951056, -0.309017, 0, 0, 0, 1, 3.26915, 10.6406, 0 > 
  texture { pigment { color rgbt <1,0.0333333,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < 0.309017, -0.951056, 0, 0.951056, 0.309017, 0, 0, 0, 1, -3.22021, 10.3316, 0 > 
  texture { pigment { color rgbt <1,0.05,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < 0.809017, -0.587785, 0, 0.587785, 0.809017, 0, 0, 0, 1, -8.28857, 6.26724, 0 > 
  texture { pigment { color rgbt <1,0.0666667,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < 1, 2.78181e-08, 0, 0, 1, 0, 0, 0, 1, -10, 6.55651e-07, 0 > 
  texture { pigment { color rgbt <1,0.0833333,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < 0.809017, 0.587785, 0, -0.587786, 0.809017, 0, 0, 0, 1, -7.70079, -6.07625, 0 > 
  texture { pigment { color rgbt <1,0.1,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < 0.309017, 0.951056, 0, -0.951056, 0.309017, 0, 0, 0, 1, -2.26915, -9.6406, 0 > 
  texture { pigment { color rgbt <1,0.116667,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < -0.309017, 0.951056, 0, -0.951057, -0.309017, 0, 0, 0, 1, 4.22021, -9.33159, 0 > 
  texture { pigment { color rgbt <1,0.133333,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < -0.809017, 0.587785, 0, -0.587786, -0.809017, 0, 0, 0, 1, 9.28857, -5.26724, 0 > 
  texture { pigment { color rgbt <1,0.15,0,0> } }
}
		
object {   
  box { <0,  0.0, 0>, <1,  1,  1> }
  matrix < -1, 0, 0, 0, -1, 0, 0, 0, 1, 11, 0.999999, 0 > 
  texture { pigment { color rgbt <1,0.166667,0,0> } }
}
		

// Done...

		