#ifndef LIBRARY_C_INCLUDED // <-- Include guards
#define LIBRARY_C_INCLUDED


// --- library file ---

// This file will be included in main.c

#define RELAY1 sys[231]
#define RELAY2 sys[232]

#define ON	1
#define OFF	0

#define isOn(what) ((what) != OFF)             // parenthesis for safety
#define setTo(what, value) what = (value)

library_function()
{
	echo("Hello.");
}

#endif
