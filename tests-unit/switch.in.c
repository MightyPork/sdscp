main() {
	switch (20) {
		case 10:
			echo("One");
			break;
		case 20:
			echo("Two");
			break;
		case 30:
			echo("Three");
			/// Fall-through
		case 40:
			/// Fall-through to default
		default:
			echo("Default");
			break;
	}

	/// --- Early default

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
