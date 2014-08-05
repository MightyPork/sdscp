// This example shows why you should pay close attention
// to parenthesising macros and macro arguments.

// Look at SDSCP output

// --- BAD ---
#define TWICE_bad(what) 2*what

// This will blow up
var Bad = TWICE_bad(10 + 10)^3;



// --- GOOD ---
#define TWICE_good(what) (2 * (what) )

// This will work just fine
var Good = TWICE_good(10 + 10)^3;
