#include "_init.c"

main() {
	var i = 15;

	/// Simple expr
	if (i == 15) {
		echo("fifteen");
	}

	// No braces
	if (i == 15)
		echo("fifteen");

	/// Variable only
	if (i) {
		echo("yes");
	}

	/// Always false
	if (0) {
		echo("Dead code");
	}

	/// Always true 1
	if (1) {
		echo("Always run 1");
	}

	// These other IFs would normally be optimized.
	// This is turned off for the test.

	/// Always true 2
	if (! 0) {
		echo("Always run 2");
	}

	/// Always true 3
	if (! (((0)))) {
		echo("Always run 3");
	}

	/// Always true 4
	if (123 == 123) {
		echo("Always run 4");
	}


	/// Simple if-else
	if (i == 12) {
		echo("yes");
	} else {
		echo("no");
	}

	/// No braces
	if (i == 12)
		echo("yes");
	else
		echo("no");

	/// 2 chained
	if (i == 1) {
		echo("One");
	} else if (i == 2) {
		echo("Two");
	}


	/// 3 chained
	if (i == 10) {
		echo("Ten");
	} else if (i == 20) {
		echo("Twenty");
	} else if (i == 30) {
		echo("Thirty");
	}

	/// 3 chained + else
	if (i == 10) {
		echo("Ten");
	} else if (i == 20) {
		echo("Twenty");
	} else if (i == 30) {
		echo("Thirty");
	} else {
		echo("Other");
	}
}
