//!!! Zero used to be treated as undefined. That is no longer the case, use #if for that!

#define DO_STUFF 0 // ignored
#define FOOBAR 1
#define BE_LAZY 1 /*
LOL
*/

main () {
#ifdef DO_STUFF
    echo("Doing stuff");
#else
    echo("Fridey");
#endif

#ifdef BE_LAZY
    echo("laying on bed");
#endif

#ifndef BE_LAZY
    echo("WORKING HARD");
#endif

							#ifdef FOOBAR
								echo("Indent is OK");
							#endif
}
