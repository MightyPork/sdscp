#pragma renderer sds2

#include "sys2.c"

#define HEATING _RELAY[1]
#define THERMO _TEMP[1]

var preset = 140;

main() {
	if(THERMO > preset) {
		HEATING = foo(0);
	} else {
		HEATING = foo(1);
	}

	wait(1000);
}

foo(a){
	return a;
}
