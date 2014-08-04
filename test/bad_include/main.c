
#include "fucked_up.c"

// When the corrupt file is included, it's content is copied to the main file.
//
// ----
// SyntaxError: Unterminated {...} block
// At: >>{ /* How pretty!  <<
// Near: >>n opening brace! */ { /* How pretty! */ <<
// ----

main()
{
	foo();
	bar();
}
