#include "_init.c"

#pragma simplify_ifs true

main() {
	var i = 15;

	/// Always false
	if (0) {
		echo("Dead code");
	}

	/// Always true 1
	if (1) {
		echo("Always run 1");
	}

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

	/// Infinite loop while
	while(1) {
		echo("Cycle");
	} // TODO optimize away "__wh_break_1"

	/// Infinite loop do-while
	do {
		echo("Cycle");
	} while(1);

	/// Do-while-false
	do {
		echo("Cycle");
	} while(0);

	/// Do-while-false with dead code
	do {
		echo("Cycle");
		break;
		echo("Foo");
	} while(0);

	/// FOR Dead code removal with continue
	for(i = 0; i < 10; i++) {
		echo("Loop");
		continue;
		echo("DEAD CODE");
	}

	/// FOR Dead code removal with break
	for(i = 0; i < 10; i++) {
		echo("Loop");
		break;
		echo("DEAD CODE");
	}//TODO the break label should also be removed
}
