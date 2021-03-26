main() {
	var c = 1122;
	var yo = 15;

	for(var i=0; i<100; i++)
		do_stuff();
	echo(" ");

	// This creates a temporary.
	// The advantage is that manipulating "c"
	// inside the switch won't cause unexpected behavior.
	switch(c) {
		case 7:
			echo("7");
			break;

		case get_magic_number():
			echo("magic");
			// Fall through

		case 111111111:
			echo("magic or 111111111");
			break;

		case yo:
			echo("yo");
			// Fall through
		case 16:
			echo("yo or 16");
			break;

		case 1+one()+yo:
			echo("1+one()+yo");
			break;

		default:
			echo("default");
	}
}

do_stuff() {
	echoinline("Stuff");
}

get_magic_number() {
	return 123456;
}

one() {return 1;}
