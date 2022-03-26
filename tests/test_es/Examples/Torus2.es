set maxobjects 160000
{ a 0.3  sat 0.5 } grinder 

set background #fff
rule grinder { 
   36 * { rz 10  y 0.1   }   36 * { ry 10  z 1.2 b 0.99 h 12  } xbox
} 

rule xbox {
  { s 1.1  } frame
  { b 0.7  color #eee   a 0.2  }  box
}

rule xbox {
 { s 1.1    } frame
 { b 0.7  color #fff  a 0.3    } box
}

#define _f3 10
#define _f1 0.05
#define _f2 1.05

rule frame  {
{ s _f1 _f2 _f1  x _f3  z _f3 } box
{s _f1 _f2 _f1 x _f3  z -_f3 } box
{ s _f1 _f2 _f1 x -_f3  z _f3} box
{s _f1 _f2 _f1 x -_f3 z -_f3} box


{ s _f2 _f1  _f1  y _f3  z _f3 } box
{ s _f2 _f1  _f1 y _f3 z -_f3 } box
{ s _f2 _f1  _f1 y -_f3  z _f3 } box
{ s _f2 _f1  _f1 y -_f3  z -_f3 } box

{ s _f1 _f1  _f2 y _f3 x _f3 } box
{ s _f1 _f1  _f2 y _f3  x -_f3 } box
{ s _f1 _f1  _f2 y -_f3  x _f3 } box
{ s _f1 _f1  _f2 y -_f3  x -_f3} box

}