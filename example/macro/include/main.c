// --- application file ---

// Include a lib
#include "library.c"

// We can use macros from library now

#define heating		RELAY1
#define ventilator 	RELAY2

#define on(x)	setTo(x, 1)
#define off(x)	setTo(x, 0)

change_mode()
{
	if (isOn(heating)) {
		off(heating);
		on(ventilator);
	} else {
		off(ventilator);
		on(heating);
	}
}
