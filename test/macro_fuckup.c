var a;
#define RELAY[n] a = 231+((n)-1); sys[a]

test()
{
	// works fine
	RELAY[6] = 1;
	
	// DOES NOT WORK
	echo( RELAY[5] );
	
	// TOTAL DISASTER
	foo = RELAY[6] + RELAY[2] ;
}
