#define ONE 1
#define TWO 2
#define ZERO 0
#define ALSO_ZERO
#define ONE_PLUS_ONE (ONE+ONE)

main () {
#if ONE
	echo("one1");
#endif

#if ONE==ONE
	echo("one2");
#endif

#if (ONE==ONE)
	echo("one is one");
#endif

#if ONE==ONE && TWO == (ONE + ONE) && TWO == ONE_PLUS_ONE
	echo("complex math");
#endif

#if defined(ONE)
	echo("ONE is defined");
#endif

#if !defined(XXXX)
	echo("XXXX is not defined");
#endif

#if defined(BLUHG) == 0
	echo("BLUHG is not defined");
#endif

#if ONE == TWO
	#error Buggy const eval in #if
#endif

#ifndef ZERO
	#error ZERO is defined but ifndef says it is't
#endif

#if defined(BANANAS)
	#error defined(BANANAS) but BANANAS is not defined
#endif
}
