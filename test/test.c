
// testing a support for flags
#define FLAG

// testing simple numeric define
#define RELE1 sys[231]
#define TEPLOTA sys[310]

#define EXPR ((14 + 76) / 13)

#define __SYS_FLASH 99
#define __SYS_FLASH_COUNT 16
#define SYS_FLASH_1 sys[100]
#define SYS_FLASH_2 sys[101]
#define SYS_FLASH_3 sys[102]

#define ADD(a, b) a + b ^^^ asshole

#define MOO(lol) echo("moo!")

#define MULTILINE(arg, boo, foo)  call_something(arg, boo); \
                                  echo("Yo dawg!", boo, foo); \
                                  call_something_else(ADD(85,boo), 37, 44, 'f')

#include "other.c"

/*
 * Here is a comment
 */

I_AM_BETWEEN_COMMENTS();
/*
and more
*/

#define UGLY_SHIT(arg, barg, marg) some stuff goes \ // comment
	and more of it \ /*yo
	dawg */ here is arg more of "stringL"marg"booo"the macro \
	and one more line barg. // comment for fun

shit();

main
{
	RELE1 = 255;
	goto home;

	if(TEPLOTA > 16) {
		sys[__SYS_FLASH + 13] = ADD(7, 15);
		MOO(123);
		MULTILINE(12, add(4, 3), "THIRD");
	}

	for(i=0; i<100; i++) {
		hereBeLions();
	}

	home:
#define ass
#ifdef FLAG
	FLAG_IS_ON;

	#ifndef ass
		moooOOoooo ass on
	#else
		YOYOYO
	#endif

#else
	// FLAG not set
	FLAG_IS_OFF;
#endif
}

