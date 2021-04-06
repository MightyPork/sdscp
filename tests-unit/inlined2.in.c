#pragma inline_one_use_functions true

// This test verifies that local variables can safely alias those in the parent function when 
// inlining

main () {
    // Called twice to avoid inlining
	inner();
	inner();
}

inner() {
    var y = 15;
	/// Level 0
	echo(sum3(1, 2, 3));
	/// End 0
	echo(y);
}

sum3(a, b, c) {
	/// Level 1
	var y = sum2(a, b);
	/// End 1
	return y + c;
}

sum2(a, b) {
	/// Level 2
	var y = add(a, b);
	/// End 2
	return y;
}

add(a, b) {
	/// Level 3
	var y = a + b;
	/// End 3
	return y;
}
