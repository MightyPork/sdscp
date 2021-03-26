main() {
	/// No braces
	while(sys[15] == 1)
		echo("Cycle");

	/// Simple
	while(sys[15] == 1) {
		echo("Cycle");
	}

	/// Infinite loop
	while(1) {
		echo("Cycle");
	}

	/// Simple do-while
	do {
		echo("Cycle");
	} while(sys[15] == 1);

	/// Infinite loop do-while
	do {
		echo("Cycle");
	} while(1);

	/// Do-while-false
	do {
		echo("Cycle");
	} while(0);

	/// Downcount
	var k = 100;
	while(k > 10) {
		k--;
		echo(k);
	}

	/// Nested
	while(1 == 1) {
		do {
			echo("yo");
		} while(2 == 2);
	}
}
