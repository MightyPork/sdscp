main()
{
	var a = 75;

	switch(a + 1) {
		case 76:
			echo("Good");
			break;
		case 99:
			echo("Bad");
		case 74:
			echo("You suck at math!");
		case 100:
			echo("Fall thru");
		//	break;
		// default:
		// 	echo("Default yo");
	}
}
