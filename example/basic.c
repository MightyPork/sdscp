#include "library/sys.c"


init()
{
	echo("Program starting.");
}


main()
{
	var on = 0; // relay state
	var last_time = _TIME_S; // macro from sys.c

	while(1)
	{
		// Loop forever

		if (_TIME_S != last_time)
		{
			last_time = _TIME_S; // remember current time

			echo("Changing relay...");
			on = 1 - on; // toggle 0<->1
			_RELAY[1] = on;	// write to relay
		}
	}
}
