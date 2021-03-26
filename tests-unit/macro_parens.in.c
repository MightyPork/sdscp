// This example shows why you should pay close attention
// to parenthesising macros and macro arguments.

// Look at SDSCP output

// --- BAD ---
#define TWICE_bad(what) 2*what



// --- GOOD ---
#define TWICE_good(what) (2 * (what) )

main () {
    echo(TWICE_bad(10 + 10)*3); // 50
    echo(TWICE_good(10 + 10)*3); // 120
}
