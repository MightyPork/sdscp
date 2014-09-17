// recurs.c was included

#ifndef MY_INCLUDE_GUARD
#define MY_INCLUDE_GUARD
// recurs.c was evaluated


// including itself, how clever...
#include "recurs.c"


// This file shows the use of Include Guards.
// If you remove the guards, you'll get infinite recursion.
//
// Check how it is evaluated - let sdscp compile it and see the output.
moo()
{
	echo("MoOooOooOO!!")
}

#endif
