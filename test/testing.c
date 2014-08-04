#define RELAY[n] sys[231+((n)-1)]

test()
{
	RELAY[6] = 1;
	echo(RELAY[5]);
}