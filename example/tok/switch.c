switch(sys[65]) {

	case 1024:
		echo("a", 64);
		break;

	case 1025:
		echo("b", 1025);
		break;

	case 1026:
		echo("b", 1026);
		break;

	default:
		echo("other", sys[65]);
}


switch(sys[xoxo+12]) {
	case 100:
	case 15:
		echo("first");
	case sys[1024 + ram[15]]:
		echo("second");
		break;
	case 0:
		echo("zero");
		break;
	default:
		echo("default branch");
}
