#pragma renderer sds2

#include "sys2.c"

#define HEATING RELAY[1]
#define THERMO TEMP[1]

var preset = 140;

main() {
	while(true) {
		if(THERMO > preset) {
			HEATING = 0;
		} else {
			HEATING = 1;
		}

		wait(1000);
	}
}
