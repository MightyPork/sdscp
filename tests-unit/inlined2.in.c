#pragma inline_one_use_functions true

// This test verifies that local variables can safely alias those in the parent function when 
// inlining

main () {
	var y = 15;
	echo(sum3(1, 2, 3));
	echo(y);
}

sum3(a, b, c) {
	var y = sum2(a, b);
	return y + c;
}

sum2(a, b) {
	var y = add(a, b);
	return y;
}

add(a, b) {
	var y = a + b;
	return y;
}
