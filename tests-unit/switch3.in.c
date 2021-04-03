main() {
	a_func(15);
}

a_func(what) {
	// This is different in that we're using a variable
	other_func();
	switch (what) {
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

// not inlined in tests
other_func() {}
