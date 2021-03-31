main() {
	switch (15) {
		case 10:
			echo("One");
			break;
		default:
			echo("Default");
			/// Fall though to 20
		case 20:
			echo("Two");
			break;
		case 30:
			echo("Three");
			break;
	}
}
