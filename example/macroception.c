// This example demonstrates the use
// of macros in other macros

// --- library file ---
#define RELAY1 sys[231]
#define RELAY2 sys[232]

#define ON 1
#define OFF 0

#define isOn(what) ((what) != OFF)

// --- application file ---

#define heating		RELAY1
#define ventilator 	RELAY2

#define on(sv) sv = 1
#define off(sv) sv = 0

// ...

change_mode()
{
	if (isOn(heating)) {
		off(heating)
		on(ventilator)
	} else {
		off(ventilator)
		on(heating)
	}
}
