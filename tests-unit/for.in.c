main() {
	/// No braces
	for(var i=0; i<10; i++)
		echo("Cycle ", i);

	/// Complex test
	var j = 150;
	/// !
	for(i = 0; i < 100 && j == 150; i++) {
		echo("Cycle ", i);
	}

	/// Empty init
	i = 0;
	/// !
	for(; i < 100; i++) {
		echo("Cycle ", i);
	}

	/// Empty init and increment
	i = 0;
  	/// !
	for(; i < 100;) {
		echo("Cycle ", i);
		i += 10;
	}

	/// Infinite loop
	for(;;) {
		echo("Loop");
	}

	/// Continue
	for(i = 0; i < 10; i++) {
		echo("Loop");
		if (sys[10]) continue;
		echo("Tail");
	}

	/// Continue inner
	for(i = 0; i < 10; i++) {
		echo("Loop");
		for(j = 0; j < 10; j++) {
			echo("Loop2");
			if (sys[10]) continue;
			echo("Tail");
		}
	}

	/// Break
	for(i = 0; i < 10; i++) {
		echo("Loop");
		if (sys[10]) break;
		echo("Tail");
	}

	/// Break inner
	for(i = 0; i < 10; i++) {
		echo("Loop");
		for(j = 0; j < 10; j++) {
			echo("Loop2");
			if (sys[10]) break;
			echo("Tail");
		}
	}
}
