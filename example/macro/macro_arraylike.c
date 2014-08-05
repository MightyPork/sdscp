
// basically function macros that look like arrays
#define squares[i] ((i)*(i))
#define cubes[i] ((i)*(i)*(i))


// This is a bad practice
// Will work for writing, but not for reading.
// SDS-C's stupid limitations force us to such hacks.
#define RELAY[i] a=230+(i);		\
                 sys[a]

#define TIMER sys[64]

#define ON 1
#define OFF 0


var a;

/**
 * This file demonstrates the use of array-like macros.
 */
main()
{
	echo("2^2 = ", squares[2])
	echo("10^3 = ", cubes[10])
	echo("10000^3 = ", cubes[10000])

	RELAY[6] = ON;

	TIMER = 6;
foo:
	if(TIMER == 0) goto foo;

	RELAY[6] = OFF;
}
