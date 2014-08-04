#define TWICE_A(what) 2*what
#define TWICE_B(what) (2 * (what) )

var Bad  = TWICE_A(10+10)^3;
var Good = TWICE_B(10+10)^3;
